"""Update UserBot code (for Indus Userbot)
Syntax: .update
\nAll Credits goes to © @Three_Cube_TeKnoways
\nFor this awasome plugin.\nPorted from PpaperPlane Extended"""

import asyncio
import os
import sys

import git

from var import Config
from indus.utils import admin_cmd, sudo_cmd, eor

# -- Constants -- #
IS_SELECTED_DIFFERENT_BRANCH = (
    "looks like a custom branch {branch_name} "
    "is being used:\n"
    "in this case, Updater is unable to identify the branch to be updated."
    "please check out to an official branch, and re-start the updater."
)
OFFICIAL_UPSTREAM_REPO = "https://github.com/Team-Indus/IndusUserbot.git"
BOT_IS_UP_TO_DATE = "`The Indus is up-to-date.\nThank you for Using this Service.`"
NEW_BOT_UP_DATE_FOUND = (
    "New Update Found for {branch_name}\n" "Changelog: \n\n{changelog}\n" "Updating ..."
)
NEW_UP_DATE_FOUND = "New Update Found For {branch_name}\n" "`Updating ...`"
REPO_REMOTE_NAME = "temponame"
IFFUCI_ACTIVE_BRANCH_NAME = "main"
DIFF_MARKER = "HEAD..{remote_name}/{branch_name}"
NO_HEROKU_APP_CFGD = "No Heroku Application Found, But a Key Given? 😕 "
HEROKU_GIT_REF_SPEC = "HEAD:refs/heads/master"
RESTARTING_APP = "Re-Starting Heroku Application"
# -- Constants End -- #


@indus.on(admin_cmd("update ?(.*)", outgoing=True))
@indus.on(sudo_cmd("update ?(.*)", allow_sudo=True))
async def updater(message):
    try:
        repo = git.Repo()
    except git.exc.InvalidGitRepositoryError as e:
        repo = git.Repo.init()
        origin = repo.create_remote(REPO_REMOTE_NAME, OFFICIAL_UPSTREAM_REPO)
        origin.fetch()
        repo.create_head(IFFUCI_ACTIVE_BRANCH_NAME, origin.refs.master)
        repo.heads.master.checkout(True)

    active_branch_name = repo.active_branch.name
    if active_branch_name != IFFUCI_ACTIVE_BRANCH_NAME:
        await eor(message,
            IS_SELECTED_DIFFERENT_BRANCH.format(branch_name=active_branch_name)
        )
        return False

    try:
        repo.create_remote(REPO_REMOTE_NAME, OFFICIAL_UPSTREAM_REPO)
    except Exception as e:
        print(e)

    temp_upstream_remote = repo.remote(REPO_REMOTE_NAME)
    temp_upstream_remote.fetch(active_branch_name)

    changelog = generate_change_log(
        repo,
        DIFF_MARKER.format(
            remote_name=REPO_REMOTE_NAME, branch_name=active_branch_name
        ),
    )

    if not changelog:
        updt = await eor(message, "`Updation in Progress......`")
        await asyncio.sleep(5)

    message_one = NEW_BOT_UP_DATE_FOUND.format(
        branch_name=active_branch_name, changelog=changelog
    )
    message_two = NEW_UP_DATE_FOUND.format(branch_name=active_branch_name)

    if len(message_one) > 4095:
        with open("change.log", "w+", encoding="utf8") as out_file:
            out_file.write(str(message_one))
        await tgbot.send_message(
            message.chat_id, document="change.log", caption=message_two
        )
        os.remove("change.log")
    else:
        await eor(message,message_one)

    temp_upstream_remote.fetch(active_branch_name)
    repo.git.reset("--hard", "FETCH_HEAD")

    if Var.HEROKU_API_KEY is not None:
        import heroku3

        heroku = heroku3.from_key(Var.HEROKU_API_KEY)
        heroku_applications = heroku.apps()
        if len(heroku_applications) >= 1:
            if Var.HEROKU_APP_NAME is not None:
                heroku_app = None
                for i in heroku_applications:
                    if i.name == Var.HEROKU_APP_NAME:
                        heroku_app = i
                if heroku_app is None:
                    await message.reply(
                        "Invalid APP Name. Please set the name of your bot in heroku in the var `HEROKU_APP_NAME.`"
                    )
                    return
                heroku_git_url = heroku_app.git_url.replace(
                    "https://", "https://api:" + Var.HEROKU_API_KEY + "@"
                )
                if "heroku" in repo.remotes:
                    remote = repo.remote("heroku")
                    remote.set_url(heroku_git_url)
                else:
                    remote = repo.create_remote("heroku", heroku_git_url)
                asyncio.get_event_loop().create_task(
                    deploy_start(tgbot, message, HEROKU_GIT_REF_SPEC, remote)
                )

            else:
                await message.reply(
                    "Please create the var `HEROKU_APP_NAME` as the key and the name of your bot in heroku as your value."
                )
                return
        else:
            await message.reply(NO_HEROKU_APP_CFGD)
    else:
        await message.reply("No heroku api key found in `HEROKU_API_KEY` var")


def generate_change_log(git_repo, diff_marker):
    out_put_str = ""
    d_form = "%d/%m/%y"
    for repo_change in git_repo.iter_commits(diff_marker):
        out_put_str += f"•[{repo_change.committed_datetime.strftime(d_form)}]: {repo_change.summary} <{repo_change.author}>\n"
    return out_put_str


async def deploy_start(tgbot, message, refspec, remote):
    await updt.edit(RESTARTING_APP)
    await updt.edit(
        "Updation Sucessfull ! Now Restarting To Finish This Process. Try `{CMD_HNDLR}alive` To Check If I Am Alive \n© @IndusBots"
    )
    await remote.push(refspec=refspec)
    await tgbot.disconnect()
    os.execl(sys.executable, sys.executable, *sys.argv)
