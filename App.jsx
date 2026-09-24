import { useEffect, useState } from "react";
import {
  PieChart, Pie, Cell, Tooltip, Legend,
  BarChart, Bar, XAxis, YAxis, CartesianGrid, ResponsiveContainer,
} from "recharts";
import {
  getTransactions, getCategorySummary, getMonthlySummary, getTotals,
} from "./api";
import "./App.css";

const COLORS = ["#4F46E5", "#22C55E", "#F59E0B", "#EF4444", "#06B6D4", "#8B5CF6", "#EC4899"];

function App() {
  const [transactions, setTransactions] = useState([]);
  const [categoryData, setCategoryData] = useState([]);
  const [monthlyData, setMonthlyData] = useState([]);
  const [totals, setTotals] = useState({ total_spent: 0, total_credited: 0, transaction_count: 0 });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchAllData = async () => {
    try {
      setLoading(true);
      const [txRes, catRes, monthRes, totalRes] = await Promise.all([
        getTransactions(),
        getCategorySummary(),
        getMonthlySummary(),
        getTotals(),
      ]);
      setTransactions(txRes.data);
      setCategoryData(catRes.data);
      setMonthlyData(monthRes.data);
      setTotals(totalRes.data);
      setError(null);
    } catch (err) {
      console.error(err);
      setError("Could not connect to backend. Is the FastAPI server running on port 8000?");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAllData();
  }, []);

  if (loading) return <div className="container"><p>Loading dashboard...</p></div>;
  if (error) return <div className="container"><p className="error">{error}</p></div>;

  return (
    <div className="container">
      <h1>AI-Powered SMS Expense Tracker</h1>

      {/* Stat cards */}
      <div className="stats-row">
        <div className="stat-card">
          <p className="stat-label">Total Spent</p>
          <p className="stat-value">₹{totals.total_spent.toFixed(2)}</p>
        </div>
        <div className="stat-card">
          <p className="stat-label">Total Credited</p>
          <p className="stat-value">₹{totals.total_credited.toFixed(2)}</p>
        </div>
        <div className="stat-card">
          <p className="stat-label">Transactions</p>
          <p className="stat-value">{totals.transaction_count}</p>
        </div>
      </div>

      {/* Charts */}
      <div className="charts-row">
        <div className="chart-box">
          <h2>Category-wise Spending</h2>
          {categoryData.length === 0 ? (
            <p>No data yet</p>
          ) : (
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={categoryData}
                  dataKey="total"
                  nameKey="category"
                  cx="50%"
                  cy="50%"
                  outerRadius={100}
                  label={(entry) => entry.category}
                >
                  {categoryData.map((_, index) => (
                    <Cell key={index} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          )}
        </div>

        <div className="chart-box">
          <h2>Month-wise Spending</h2>
          {monthlyData.length === 0 ? (
            <p>No data yet</p>
          ) : (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={monthlyData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="total" fill="#4F46E5" />
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>
      </div>

      {/* Transaction table */}
      <div className="table-box">
        <h2>Recent Transactions</h2>
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>Merchant</th>
              <th>Category</th>
              <th>Payment Method</th>
              <th>Type</th>
              <th>Amount</th>
            </tr>
          </thead>
          <tbody>
            {transactions.map((tx) => (
              <tr key={tx.id}>
                <td>{tx.date}</td>
                <td>{tx.merchant}</td>
                <td>{tx.category}</td>
                <td>{tx.payment_method}</td>
                <td className={tx.transaction_type === "credit" ? "credit" : "debit"}>
                  {tx.transaction_type}
                </td>
                <td>₹{tx.amount.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;