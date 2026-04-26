import { useEffect, useMemo, useState } from 'react';

const apiBase = import.meta.env.VITE_API_BASE_URL;

export default function App() {
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState([]);
  const [step, setStep] = useState(0);
  const [feedback, setFeedback] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadQuestions() {
      const res = await fetch(`${apiBase}/api/questions`);
      const data = await res.json();
      setQuestions(data.questions ?? []);
      setLoading(false);
    }

    loadQuestions().catch(() => setLoading(false));
  }, []);

  const current = questions[step];
  const selectedAnswer = useMemo(
    () => answers.find((item) => item.questionId === current?.id)?.answerIndex,
    [answers, current]
  );

  const onSelect = (answerIndex) => {
    if (!current) return;

    setAnswers((prev) => {
      const other = prev.filter((item) => item.questionId !== current.id);
      return [...other, { questionId: current.id, answerIndex }];
    });
  };

  const onNext = () => {
    if (step < questions.length - 1) {
      setStep((s) => s + 1);
    }
  };

  const onSubmit = async () => {
    const res = await fetch(`${apiBase}/api/submit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ answers })
    });

    const data = await res.json();
    setFeedback(data.feedback ?? []);
  };

  if (loading) return <main className="shell">Loading…</main>;
  if (!questions.length) return <main className="shell">No questions available.</main>;

  if (feedback.length) {
    return (
      <main className="shell">
        <h1>Summary</h1>
        <ul>
          {feedback.map((item) => (
            <li key={item.questionId}>{item.feedback}</li>
          ))}
        </ul>
      </main>
    );
  }

  return (
    <main className="shell">
      <h1>Founder Readiness Quiz</h1>
      <p className="question">{current.question}</p>
      <div className="options">
        {current.options.map((option, idx) => (
          <button
            key={option}
            type="button"
            className={selectedAnswer === idx ? 'option selected' : 'option'}
            onClick={() => onSelect(idx)}
          >
            {option}
          </button>
        ))}
      </div>

      <div className="actions">
        <button type="button" onClick={() => setStep((s) => Math.max(0, s - 1))} disabled={step === 0}>
          Back
        </button>

        {step < questions.length - 1 ? (
          <button type="button" onClick={onNext} disabled={selectedAnswer === undefined}>
            Next
          </button>
        ) : (
          <button type="button" onClick={onSubmit} disabled={answers.length !== questions.length}>
            Finish
          </button>
        )}
      </div>
    </main>
  );
}
