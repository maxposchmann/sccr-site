from flask import Flask
from config import Config

server = Flask(__name__)
server.config.from_object(Config)

from flask import Blueprint, render_template, redirect, request, url_for
from flask_bootstrap import Bootstrap

bootstrap = Bootstrap(server)
server_bp = Blueprint('main', __name__)

from forms import selectTeam
import pandas as pd

db = 'SelfConsistentCFBRanker/ncaafb.p'
d = pd.read_pickle(db)

def formatDf(data):
    a = data.copy()
    df = pd.DataFrame(a) \
        .to_html(classes='table table-striped sortable', index=False, border=0, justify='left', escape=False)
    return df

def teamLink(teamName):
    x = ''.join([i for i in teamName if not i.isdigit()]).strip()
    return f'<a href="/team_stats?team={x}">{teamName}</a>'

@server_bp.route('/',methods=['GET', 'POST'])
def index():
    table = d['analysis']['teamRankings'].copy()
    table['Team'] = table['Team'].apply(lambda x: teamLink(x))
    table =formatDf(table)

    week = d['analysis']['week']
    return render_template('index.html', title='Index', table=table, week=week)

@server_bp.route('/team_stats',methods=['GET', 'POST'])
def team_stats():
    form = selectTeam()
    form_team = form.team.data
    link_team = request.args.get('team')

    if form_team == None and link_team == None:
        return render_template('selectTeam.html', form=form)
    elif form_team == link_team or form_team == None:
        if form.team.data == None:
            form.team.data = link_team
        team = form.team.data
        try:
            data = d['analysis']['byTeam'][team]
            stats = d['analysis']['byTeam'][team]['stats'].copy()
            stats = formatDf(stats)
            results = d['analysis']['byTeam'][team]['results'].copy()
            try:
                results['Played'] = results['Played'].apply(lambda x: teamLink(x))
            except:
                pass
            results = formatDf(results)
            remaining = d['analysis']['byTeam'][team]['remaining'].copy()
            try:
                remaining['Remaining'] = remaining['Remaining'].apply(lambda x: teamLink(x))
            except:
                pass
            remaining = formatDf(remaining)

            if request.method == "POST":
                team = form.team.data
                data = d['analysis']['byTeam'][team]
            return render_template('teamStats.html', data=data, form=form, stats=stats, results=results, remaining=remaining)
        except KeyError:
            return redirect(f'/team_stats')
    else:
        if form.team.data == None:
            form.team.data = link_team
        team = form.team.data
        return redirect(f'/team_stats?team={team}')

@server_bp.route('/explanation',methods=['GET', 'POST'])
def explanation():
    return render_template('explanation.html')

server.register_blueprint(server_bp)
