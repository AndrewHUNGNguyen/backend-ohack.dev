from datetime import datetime
from ratelimit import limits
from common.utils.slack import invite_user_to_channel, send_slack, send_slack_audit
from model.problem_statement import ProblemStatement
from model.user import User
from db.db import delete_helping, insert_helping, delete_problem_statement, fetch_problem_statement, insert_problem_statement, update_problem_statement
import logging
import pytz
from cachetools import cached, LRUCache, TTLCache
from cachetools.keys import hashkey
import uuid
from services import users_service

logger = logging.getLogger("ohack")

#TODO consts file?
ONE_MINUTE = 1*60

@limits(calls=50, period=ONE_MINUTE)
def save_problem_statement(d):
    logger.debug("Problem Statement Save")

    p = ProblemStatement() # Don't use ProblemStatement.deserialize here. We don't have an id yet.
    p.update(d)

    p = insert_problem_statement(p)

    send_slack_audit(action="save_problem_statement",
                     message="Saving", payload=d)

    return p

@limits(calls=50, period=ONE_MINUTE)
def update_problem_statement_fields(d):
    
    problem_statement = None
    if 'id' in d and d['id'] is not None:
        problem_statement = fetch_problem_statement(d['id'])
    
    if problem_statement is not None:
        problem_statement.update(d)
        problem_statement.id = d['id']
        return update_problem_statement(problem_statement)
    else:
        return None
    
def get_problem_statement(id):
    return fetch_problem_statement(id)

def remove_problem_statement(id):
    return delete_problem_statement(id)

@limits(calls=100, period=ONE_MINUTE)
def save_helping_status(propel_user_id, d):
    logger.info(f"save_helping_status {propel_user_id} // {d}")
    user = users_service.get_user_from_propel_user_id(propel_user_id)

    slack_message = None

    # Do the actual data wrangling
    problem_statement = save_user_helping_status(user, d)

    problem_statement_title = problem_statement.title
    problem_statement_slack_channel = problem_statement.slack_channel

    helping_status = d["status"] # helping or not_helping

    problem_statement_id = d["problem_statement_id"]

    npo_id =  d["npo_id"] if "npo_id" in d else ""

    mentor_or_hacker = d["type"]

    url = ""
    if npo_id == "":
        url = f"for project https://ohack.dev/project/{problem_statement_id}"
    else:
        url = f"for nonprofit https://ohack.dev/nonprofit/{npo_id} on project https://ohack.dev/project/{problem_statement_id}"


    slack_user_id = None
    try:
        slack_user_id = user.user_id.split("-")[1]  # Example user_id = oauth2|slack|T1Q7116BH-U041117EYTQ
        invite_user_to_channel(user_id=slack_user_id,
                            channel_name=problem_statement_slack_channel)
    except Exception:
        pass # Don't return error if slack invite fails.


    if slack_user_id is not None:
        try:
            slack_message = f"<@{slack_user_id}>"

            if "helping" == helping_status:
                slack_message = f"{slack_message} is helping as a *{mentor_or_hacker}* on *{problem_statement_title}* {url}"
            else:
                slack_message = f"{slack_message} is _no longer able to help_ on *{problem_statement_title}* {url}"

            send_slack(message=slack_message,
                    channel=problem_statement_slack_channel)
        except:
            pass # Don't return error if slack message fails.

    return problem_statement

def save_user_helping_status(user: User, d):

    logger.info(f"save_user_helping_status {user.serialize()} // {d}")
    helping_status = d["status"] # helping or not_helping
    
    problem_statement_id = d["problem_statement_id"]
    mentor_or_hacker = d["type"]

    helping_date = datetime.now().isoformat()
    
    to_add = {
        "user": user.id,
        "slack_user": user.user_id,
        "type": mentor_or_hacker,
        "timestamp": helping_date
    }
    
    try: 
        send_slack_audit(action="helping", message=user.user_id, payload=to_add)
    except Exception:
        pass

    problem_statement: ProblemStatement | None = None
  
    if "helping" == helping_status:
        problem_statement = insert_helping(problem_statement_id, user, mentor_or_hacker, helping_date)
    else:
        problem_statement = delete_helping(problem_statement_id, user)

    return problem_statement

@cached(cache=TTLCache(maxsize=100, ttl=600))
def get_problem_statement_by_id(id):
    logger.debug(f"get_problem_statement_by_id start project_id={id}")    
    
    problem_statement: ProblemStatement | None = fetch_problem_statement(id)
    
    if problem_statement is None:
        logger.warning("get_problem_statement_by_id end (no results)")
    else:                                
        logger.info(f"get_problem_statement_by_id end (with result):{problem_statement}")
        
    return problem_statement