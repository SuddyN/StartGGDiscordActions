# Start.GG Discord Bot for State-Wide Offline Tournaments

This project combines GitHub Actions, the Start.GG GraphQL API, and Discord Webhooks to create a listing tool for all upcoming offline events of a given game in a given region.

The tool is not hosted 24/7 like a typical discord bot. It runs via a periodic GitHub action, scheduled for 9PM EST every night.

It posts the events taking place the next day. On Sundays, it also posts the events for the next week, and if an event was created during the week after the weekly listing, it posts that event the day it was created.

# Using This Tool

Running this is not like most Discord apps, since it relies on GitHub actions as a host. To add this tool in your own servers, you will need to:

## Fork this repository

From the main repository page (where you probably are now):

- Click `Fork`
- Uncheck `Copy the main branch only`
- Create the fork

## Set up GitHub Actions

- From the new repository page on GitHub, click the `Actions` tab.
- Click "I understand my workflows, go ahead and enable them".
- In the resulting page, under the Actions toolbar on the left, click `Discord Webhook`.
- In the yellow warning, click `Enable Workflow`.
- At the top of the page under the `Discord Webhook` title, click `main.yml` to open the editor.
- In the editor, edit the attributes for `STATE`, `TIMEZONE`, and `GAME_ID` under `jobs:` `build:` `steps:` `- name: Running Script` `env:`.
  - `STATE`: 2-letter state code representing your state in the USA. If you want to expand this or use other regions, you're going to have to edit the code in `app.py` and figure it out yourself because I can't be bothered.
  - `TIMEZONE`: timezone code. my reccommendation is that you leave this on EST even if you're not EST because I haven't tested anything different, and designed the app assuming it would be running on EST, but other timezone codes should work. Reference the `pytz` python package for a list of valid timezones.
  - `GAME_ID`: Start.GG backend ID for game title.
    - Rivals 2 - `53945`
    - Rivals of Aether - `24`
    - Super Smash Bros. Ultimate - `1386`
    - Super Smash Bros. Melee - `1`
    - HewDraw Remix - `34157`
    - Project+ - `33602`
    - Project M - `2`
    - Super Smash Bros. for Wii U - `3`
    - Super Smash Bros. Brawl - `5`
    - Super Smash Bros. (64) - `4`
    - MultiVersus - `40849`
    - Brawlhalla - `15`
    - Street Fighter 6 - `43868`
    - Street Fighter V - `10055`
    - Ultra Street Fighter IV - `16`
    - Street Fighter III: 3rd Strike - `610`
    - TEKKEN 8 - `49783`
    - TEKKEN 7 - `17`
    - Guilty Gear: Strive - `33945`
    - Guilty Gear Xrd REV2 - `36`
    - Guilty Gear XX Accent Core Plus R - `22406`
    - The King of Fighters XV - `36963`
    - DRAGON BALL FighterZ - `287`
    - Under Night In-Birth II Sys:Celes - `50203`
    - Granblue Fantasy Versus: Rising - `48548`
    - Mortal Kombat 1 - `48599`
    - Marvel vs. Capcom: Infinite - `288`
    - Ultimate Marvel vs Capcom 3 - `18`
    - Marvel Vs. Capcom 2 - `3742`
    - Skullgirls: 2nd Encore - `32`
    - If you want to change this to another game here's the documentation good luck: https://developer.start.gg/docs/examples/queries/videogame-id-by-name

## Add repository secrets

In order to run the tool, you also need access to a Start.GG developer token (to access the Start.GG GraphQL API) and a Discord Webhook (where the tool publishes event info).

These are secret and should not be shared with anyone or stored anywhere others can access them.

- From the repository page on GitHub, click the `Settings` tab.
- Under `Security` in the left toolbar, click `Secrets and variables` and then click `Actions`.

This should bring you to the `Actions secrets and variables` page where we can add the last two required environment variables.

### Create a Discord Webhook

Here's the Discord Webhook documentation: https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks

- Go make a webhook for the channel you want updates in, copy the webhook URL, and come back to the `Actions secrets and variables` page.
- Under `Repository secrets`, click `New repository secret`.
- Set `Name` to `WEBHOOK_URL`, and set `Secret` to the webhook URL you copied.
- Click `Add Secret`.

### Create Start.GG Authentication Token

Heres the Start.GG Authentication documentation: https://developer.start.gg/docs/authentication

- Go create a token and copy it, then back to the `Actions secrets and variables` page.
- Under `Repository secrets`, click `New repository secret`.
- Set `Name` to `STARTGG_TOKEN`, and set `Secret` to the token you copied.
- Click `Add Secret`.

## Test the project

To test that everything is working: 

- From the new repository page on GitHub, click the `Actions` tab.
- Under the Actions toolbar on the left, click `Discord Webhook`.
- Click the `Run workflow` dropdown, and then the green `Run workflow` button.

You should see posts for today's events posted in your discord channel.
