import express from 'express';
import cors from 'cors';
import { PrismaClient } from '@prisma/client';
import { questions } from './questions.js';

const app = express();
const prisma = new PrismaClient();
const port = process.env.PORT || 8080;

app.use(cors({ origin: process.env.CORS_ORIGIN?.split(',') ?? '*' }));
app.use(express.json({ limit: '200kb' }));

app.get('/health', (_, res) => {
  res.json({ ok: true });
});

app.get('/api/questions', (_, res) => {
  const sanitizedQuestions = questions.map(({ feedback, ...rest }) => rest);
  res.json({ questions: sanitizedQuestions });
});

app.post('/api/submit', async (req, res) => {
  const { answers } = req.body;
  if (!Array.isArray(answers)) {
    return res.status(400).json({ error: 'answers must be an array' });
  }

  const normalizedAnswers = answers
    .map(({ questionId, answerIndex }) => ({ questionId: Number(questionId), answerIndex: Number(answerIndex) }))
    .filter(({ questionId, answerIndex }) => Number.isInteger(questionId) && Number.isInteger(answerIndex));

  const feedback = normalizedAnswers
    .map(({ questionId, answerIndex }) => {
      const q = questions.find((item) => item.id === questionId);
      if (!q || !q.feedback[answerIndex]) return null;
      return { questionId, feedback: q.feedback[answerIndex] };
    })
    .filter(Boolean);

  const attempt = await prisma.quizAttempt.create({
    data: { answers: normalizedAnswers }
  });

  return res.json({ attemptId: attempt.id, feedback });
});

app.use((err, _req, res, _next) => {
  // eslint-disable-next-line no-console
  console.error(err);
  res.status(500).json({ error: 'internal_server_error' });
});

app.listen(port, () => {
  // eslint-disable-next-line no-console
  console.log(`API listening on ${port}`);
});
