function App() {
  const [timestamp, setTimestamp] = React.useState(Date.now());

  const refreshImage = () => {
    setTimestamp(Date.now()); // Forces image reload
  };

  return (
    <div>
      <h2>📊 Confusion Matrix</h2>
      <img
        src={`http://localhost:5000/sensor_plot.png?t=${timestamp}`}
        alt="Sensor Data Plot"
      />
      <br />
      <button onClick={refreshImage}>🔄 Refresh Matrix</button>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);