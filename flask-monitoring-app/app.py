from flask import Flask, render_template
import psutil
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from datetime import datetime

app = Flask(__name__)

# Function to fetch system metrics
def get_system_metrics():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cpu_percent = psutil.cpu_percent(interval=1)
    mem_percent = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/')

    return current_time, cpu_percent, mem_percent, disk_usage

# Function to create CPU and Memory Usage Graphs
def create_cpu_memory_graphs():
    times = []
    cpu_usage = []
    mem_usage = []
    for i in range(10):  # Example data for the last 10 seconds
        times.append(datetime.now().strftime("%H:%M:%S"))
        cpu_usage.append(psutil.cpu_percent(interval=1))
        mem_usage.append(psutil.virtual_memory().percent)

    # Create subplots
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1)
    fig.add_trace(go.Scatter(x=times, y=cpu_usage, mode='lines+markers', name='CPU Usage (%)'), row=1, col=1)
    fig.add_trace(go.Scatter(x=times, y=mem_usage, mode='lines+markers', name='Memory Usage (%)'), row=2, col=1)

    fig.update_layout(title='CPU and Memory Usage Over Time',
                      xaxis_title='Time',
                      yaxis_title='Usage (%)',
                      showlegend=True)

    return fig

# Function to create Disk Usage Graph
def create_disk_usage_graph():
    labels = ['Used', 'Free']
    values = [psutil.disk_usage('/').used, psutil.disk_usage('/').free]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    fig.update_layout(title='Disk Usage',
                      showlegend=True)

    return fig

# Route for the dashboard
@app.route('/')
def dashboard():
    current_time, cpu_percent, mem_percent, disk_usage = get_system_metrics()
    cpu_memory_fig = create_cpu_memory_graphs()
    disk_fig = create_disk_usage_graph()

    return render_template('dashboard.html',
                           current_time=current_time,
                           cpu_percent=cpu_percent,
                           mem_percent=mem_percent,
                           disk_percent=disk_usage.percent,
                           cpu_memory_fig=cpu_memory_fig.to_html(full_html=False),
                           disk_fig=disk_fig.to_html(full_html=False))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
