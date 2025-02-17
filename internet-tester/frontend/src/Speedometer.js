import React, { useState, useEffect } from "react";
import axios from "axios";
import { RadialBarChart, RadialBar, Legend } from "recharts";

export default function Speedometer() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [partialData, setPartialData] = useState({
    download: 0,
    upload: 0,
    ping: 0,
    jitter: 0,
  });

  const iniciarTeste = async () => {
    setLoading(true);
    setPartialData({ download: 0, upload: 0, ping: 0, jitter: 0 });
    try {
      const response = await axios.get("http://127.0.0.1:8000/medir_internet");
      const data = response.data;
      setData(data);

      // Simulate real-time data update
      let steps = 20; // Number of steps for the animation
      let stepDuration = 100; // Duration of each step in milliseconds
      let currentStep = 0;

      let interval = setInterval(() => {
        currentStep++;
        setPartialData({
          download: Math.min((data.download / steps) * currentStep, data.download),
          upload: Math.min((data.upload / steps) * currentStep, data.upload),
          ping: Math.min((data.ping / steps) * currentStep, data.ping),
          jitter: Math.min((data.jitter / steps) * currentStep, data.jitter),
        });

        if (currentStep >= steps) {
          clearInterval(interval);
          setLoading(false);
        }
      }, stepDuration);
    } catch (error) {
      console.error("Erro ao testar a internet", error);
      setLoading(false);
    }
  };

  const chartData = [
    { name: "Download", value: partialData.download, fill: "#8884d8" },
    { name: "Upload", value: partialData.upload, fill: "#82ca9d" },
    { name: "Ping", value: partialData.ping, fill: "#ff7300" },
    { name: "Jitter", value: partialData.jitter, fill: "#d0ed57" },
  ];

  return (
    <div className="flex flex-col items-center justify-center p-5">
      <h1 className="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-500 to-indigo-600 mb-4 text-center">
        Teste de Velocidade da Internet
      </h1>
      <button
        onClick={iniciarTeste}
        disabled={loading}
        className="px-6 py-3 bg-gradient-to-r from-blue-500 to-indigo-600 text-white font-semibold rounded-lg shadow-md hover:from-blue-600 hover:to-indigo-700 disabled:bg-gray-400 transition duration-300"
      >
        {loading ? "Testando..." : "Iniciar Teste"}
      </button>

      {data && (
        <div className="mt-6 flex flex-col items-center">
          <RadialBarChart
            width={300}
            height={150}
            innerRadius="10%"
            outerRadius="100%"
            startAngle={180}
            endAngle={0}
            data={chartData}
          >
            <RadialBar
              minAngle={15}
              background
              clockWise
              dataKey="value"
              animationBegin={0}
              animationDuration={1500}
            />
            <Legend iconSize={10} layout="horizontal" align="center" />
          </RadialBarChart>

          <p className="text-lg mt-4 text-center">📡 Download: {partialData.download.toFixed(2)} Mbps</p>
          <p className="text-lg text-center">🚀 Upload: {partialData.upload.toFixed(2)} Mbps</p>
          <p className="text-lg text-center">⚡ Ping: {partialData.ping.toFixed(2)} ms</p>
          <p className="text-lg text-center">📉 Jitter: {partialData.jitter.toFixed(2)} ms</p>
          <p className="text-lg text-center">❌ Perda de Pacotes: {data.perda_pacotes} %</p>
        </div>
      )}
    </div>
  );
}