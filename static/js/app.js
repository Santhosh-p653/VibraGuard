function Dashboard() {
  const [data, setData] = React.useState([]);
  const [latest, setLatest] = React.useState(0);
  const [status, setStatus] = React.useState("Online");
  const chartRef = React.useRef(null);

  React.useEffect(() => {
    const ctx = document.getElementById('vibrationChart').getContext('2d');
    chartRef.current = new Chart(ctx, {
      type: 'line',
      data: { labels: [], datasets: [{ label: 'Vibration', data: [], borderColor: 'green', backgroundColor: 'rgba(0,255,0,0.1)', fill: true }] },
      options: { animation: false, responsive: true, scales: { y: { beginAtZero: true } } }
    });

    let lastUpdate = Date.now();

    const interval = setInterval(async () => {
      try {
        const res = await fetch("/vibration/history/30");
        const readings = await res.json();
        if (readings.length > 0) lastUpdate = Date.now();

        chartRef.current.data.labels = readings.map(r => r.timestamp.split(' ')[1]);
        chartRef.current.data.datasets[0].data = readings.map(r => r.value);
        chartRef.current.update();

        setData(readings);
        const latestValue = readings.length ? readings[readings.length - 1].value : 0;
        setLatest(latestValue);

        if (latestValue > 7) setStatus("⚠ ALERT: Vibration High!");
        else setStatus("Online");

        if (Date.now() - lastUpdate > 5000)
          setStatus("⚠ Hardware Offline / Power Failure");

      } catch (err) {
        console.error(err);
        setStatus("⚠ Hardware Offline / Error");
      }
    }, 1000);

    return () => clearInterval(interval);
  }, []); // run only once on mount

  return (
    <div>
      <h1>VibraGuard Dashboard</h1>
      <h2 className="status">{status}</h2>
      <canvas id="vibrationChart" width="600" height="300"></canvas>

      <div className="bar">
        <div className="bar-fill" style={{ width: `${latest*10}%`, background: latest>7 ? 'red':'green' }}></div>
      </div>
      <h3>Latest Reading: {latest}</h3>

      <table>
        <thead>
          <tr><th>Timestamp</th><th>Vibration</th></tr>
        </thead>
        <tbody>
          {data.map((r, i) => (
            <tr key={i}>
              <td>{r.timestamp}</td>
              <td>{r.value}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<Dashboard />);
