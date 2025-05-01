import { useState, useEffect } from "react";
import questions from "./data/questions.json";

type Question = {
  id: string;
  question: string[];
  section: string;
  image: string;
};

function QuestionCard({
  question,
  show,
  onToggleCheck,
  checked,
}: {
  question: Question;
  show: boolean;
  onToggleCheck: (id: string) => void;
  checked: boolean;
}) {
  if (!show) return null;
  return (
    <div className="bg-white p-4 rounded-2xl shadow-xl mb-4">
      <div className="flex justify-between items-center mb-2">
        <h2 className="text-xl font-semibold">{question.id}</h2>
        <label className="flex items-center space-x-2 text-sm text-gray-600">
          <input
            type="checkbox"
            checked={checked}
            onChange={() => onToggleCheck(question.id)}
          />
          <span>需要校正</span>
        </label>
      </div>
      <img
        src={`/assets/images/${question.image.split("/").pop()}`}
        alt={`Question ${question.id}`}
        className="w-full rounded-xl mb-3 border"
      />
      <div className="space-y-2">
        {question.question.map((line, index) => (
          <p key={index} className="text-base text-gray-800">
            {line}
          </p>
        ))}
      </div>
      <p className="text-sm text-gray-500 mt-4">📘 {question.section}</p>
    </div>
  );
}

export default function App() {
  const [data, setData] = useState<Question[]>([]);
  const [search, setSearch] = useState("");
  const [sectionFilter, setSectionFilter] = useState("");
  const [checkedItems, setCheckedItems] = useState<Record<string, boolean>>({});

  useEffect(() => {
    setData(questions.exercises as Question[]); // 確保只取出 exercises 陣列
  }, []);

  const handleToggleCheck = (id: string) => {
    setCheckedItems((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  const sections = Array.from(new Set(data.map((q) => q.section)));

  const filtered = data.filter((q) => {
    const matchSearch =
      q.id.toLowerCase().includes(search.toLowerCase()) ||
      q.question.join(" ").toLowerCase().includes(search.toLowerCase());
    const matchSection = sectionFilter === "" || q.section === sectionFilter;
    return matchSearch && matchSection;
  });

  return (
    <div className="bg-gray-50 min-h-screen p-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">🧪 題庫瀏覽系統</h1>

        <div className="mb-6 flex flex-col md:flex-row md:items-center md:space-x-4 space-y-2 md:space-y-0">
          <input
            type="text"
            placeholder="搜尋題號或關鍵字..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full md:w-1/2 border rounded-md px-3 py-2"
          />
          <select
            className="w-full md:w-1/2 border rounded-md px-3 py-2 text-sm"
            value={sectionFilter}
            onChange={(e) => setSectionFilter(e.target.value)}
          >
            <option value="">全部章節</option>
            {sections.map((sec, idx) => (
              <option key={idx} value={sec}>
                {sec}
              </option>
            ))}
          </select>
        </div>

        {filtered.map((q, idx) => (
          <QuestionCard
            key={idx}
            question={q}
            show={true}
            onToggleCheck={handleToggleCheck}
            checked={checkedItems[q.id] || false}
          />
        ))}
      </div>
    </div>
  );
}
