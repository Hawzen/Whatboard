import dash_html_components as html
from app import app
from dashboard import dashboard

content = html.Div(id="page-content")

app.layout = dashboard.layout


if __name__ == "__main__":
    app.run_server(debug=True, port=4200)
