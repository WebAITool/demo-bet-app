const jsonServer = require('json-server');
const bodyParser = require('body-parser');
const { v4: uuidv4 } = require('uuid');
const cookieParser = require('cookie-parser');

const server = jsonServer.create();
const router = jsonServer.router('db.json');
const middlewares = jsonServer.defaults();

server.use((req, res, next) => {
  setTimeout(next, 500);
});

server.use((req, res, next) => {
  const origin = 'http://localhost:5173';
  res.header('Access-Control-Allow-Origin', origin);
  res.header('Access-Control-Allow-Credentials', 'true');
  res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With, Accept');
  res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS');
  res.header('Vary', 'Origin');

  if (req.method === 'OPTIONS') {
    return res.sendStatus(204);
  }
  next();
});

server.use(bodyParser.json());
 
server.use(cookieParser());

server.post('/auth/register', (req, res) => {
  const { login, password, email } = req.body || {};
  const db = router.db;

  const emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!login || !password || !email) {
    return res.status(422).json({ error: 'Validation failed: login, password, email are required' });
  }
  if (!emailRe.test(String(email))) {
    return res.status(422).json({ error: 'Validation failed: invalid email' });
  }
  if (String(login).length < 3) {
    return res.status(422).json({ error: 'Validation failed: login too short' });
  }
  if (String(password).length < 3) {
    return res.status(422).json({ error: 'Validation failed: password too short' });
  }

  const existingByLogin = db.get('users').find({ login }).value();
  const existingByEmail = db.get('users').find({ email }).value();
  if (existingByLogin || existingByEmail) {
    return res.status(409).json({ error: 'User with this login or email already exists' });
  }

  db.get('verification_codes').remove({ email }).write();
  const code = Math.floor(1000 + Math.random() * 9000).toString();
  db.get('verification_codes').push({ email, code, login, password, attempts: 0, created_at: new Date().toISOString() }).write();

  return res.status(200).json({ message: 'Verification code sent to email' });
});

server.post('/auth/check_code', (req, res) => {
  const body = req.body || {};
  const { email, code: providedCode } = body;
  const db = router.db;

  if (!email) {
    return res.status(400).json({ error: 'Missing email' });
  }
  if (!providedCode) {
    return res.status(400).json({ error: 'Missing code' });
  }

  const entry = db.get('verification_codes').find({ email }).value();
  if (!entry) {
    return res.status(404).json({ error: 'No code for this email' });
  }

  const MAX_ATTEMPTS = 5;
  const attempts = Number(entry.attempts || 0);
  if (attempts >= MAX_ATTEMPTS) {
    db.get('verification_codes').remove({ email }).write();
    return res.status(429).json({ error: 'Too many attempts. Code invalidated, request a new one' });
  }

  if (String(entry.code) !== String(providedCode)) {
    db.get('verification_codes')
      .find({ email })
      .assign({ attempts: attempts + 1 })
      .write();
    return res.status(400).json({ error: 'Invalid code' });
  }

  let user = db.get('users').find({ email }).value();
  if (!user) {
    const userId = (db.get('users').value().slice(-1)[0]?.id || 0) + 1;
    const login = entry.login || (email.split('@')[0]);
    const password = entry.password || '';
    user = { id: userId, email, login, password, balance: 1000 };
    db.get('users').push(user).write();
  }

  const sessionId = uuidv4();
  db.get('sessions').push({
    id: sessionId,
    userId: user.id,
    expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000)
  }).write();

  db.get('verification_codes').remove({ email }).write();

  res.cookie('session_id', sessionId, {
    httpOnly: true,
    maxAge: 7 * 24 * 60 * 60 * 1000,
    sameSite: 'lax'
  });

  return res.status(200).json({ message: 'Registration successful' });
});

 

const handleLogin = (body, res) => {
  const { login, password } = body || {};
  const db = router.db;

  if (!login || !password) {
    return res.status(400).json({ error: 'Bad request' });
  }

  const user = db.get('users').find({ login }).value();
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }

  const storedPassword = user.password ?? '';
  if (String(password) !== String(storedPassword)) {
    return res.status(400).json({ error: 'Wrong password' });
  }

  const sessionId = uuidv4();
  db.get('sessions').push({
    id: sessionId,
    userId: user.id,
    expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000)
  }).write();

  res.cookie('session_id', sessionId, {
    httpOnly: true,
    maxAge: 7 * 24 * 60 * 60 * 1000, // 7 days
    sameSite: 'lax'
  });

  return res.status(200).json({ message: 'Login successful' });
};

const authenticate = (req, res, next) => {
  const sessionId = req.cookies?.session_id || req.headers.authorization?.split(' ')[1];
  
  if (!sessionId) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  
  const db = router.db;
  const session = db.get('sessions').find({ id: sessionId }).value();
  
  if (!session || new Date(session.expiresAt) < new Date()) {
    return res.status(401).json({ error: 'Session expired' });
  }
  
  const user = db.get('users').find({ id: session.userId }).value();
  if (!user) {
    return res.status(401).json({ error: 'User not found' });
  }
  
  req.user = user;
  next();
};

const tryGetUser = (req) => {
  const sessionId = req.cookies?.session_id || req.headers.authorization?.split(' ')[1];
  if (!sessionId) return null;
  const db = router.db;
  const session = db.get('sessions').find({ id: sessionId }).value();
  if (!session || new Date(session.expiresAt) < new Date()) return null;
  const user = db.get('users').find({ id: session.userId }).value();
  return user || null;
};

server.get('/user/balance', authenticate, (req, res) => {
  res.status(200).send(req.user.balance.toString());
});

 

server.get('/user/info', authenticate, (req, res) => {
  res.status(200).json({ login: req.user.login, password: req.user.password });
});

server.post('/user/info', authenticate, (req, res) => {
  const { login, password } = req.body || {};
  const db = router.db;
  const patch = {};
  if (typeof login === 'string' && login.trim()) patch.login = login;
  if (typeof password === 'string' && password.trim()) patch.password = password;
  if (Object.keys(patch).length) {
    db.get('users').find({ id: req.user.id }).assign(patch).write();
  }
  const fresh = db.get('users').find({ id: req.user.id }).value();
  res.status(200).json({ login: fresh.login, password: fresh.password });
});

server.get('/events/all', (req, res) => {
  const db = router.db;
  const events = db.get('events')
    .filter(event => new Date(event.ended_at) > new Date())
    .map(({ id, name, ended_at, outcomes }) => ({
      event_id: id,
      name,
      ended_at,
      outcomes: outcomes.map(({ id, name, coefficient }) => ({
        name,
        coefficient
      }))
    }))
    .value();
  
  res.json(events);
});

 

server.get('/events/:id', (req, res) => {
  const db = router.db;
  const event = db.get('events').find({ id: parseInt(req.params.id) }).value();
  
  if (!event) {
    return res.status(400).json({ error: 'Event not found' });
  }
  
  const maybeUser = tryGetUser(req);
  const isAuthor = !!(maybeUser && event.author_id && event.author_id === maybeUser.id);

  res.json({
    name: event.name,
    description: event.description || '',
    ended_at: event.ended_at,
    final_outcome_id: event.final_outcome_id,
    outcomes: event.outcomes.map(({ id, name, coefficient }) => {
      let totalSize = null;
      if (isAuthor) {
        const sum = db.get('bets')
          .filter({ event_id: event.id, outcome_id: id })
          .map(b => (b.size ?? b.amount ?? 0))
          .value()
          .reduce((a, b) => a + b, 0);
        totalSize = sum;
      }
      return {
        outcome_id: id,
        name,
        total_size: totalSize,
        coefficient
      };
    })
  });
});

 

server.get('/events/my/all', authenticate, (req, res) => {
  const db = router.db;
  const items = db.get('events')
    .filter({ author_id: req.user.id })
    .map(e => ({
      event_id: e.id,
      name: e.name,
      ended_at: e.ended_at,
      final_outcome_name: (e.final_outcome_id ? (e.outcomes.find(o => o.id === e.final_outcome_id)?.name || null) : null)
    }))
    .value();
  res.status(200).json(items);
});

 

server.post('/events/my', authenticate, (req, res) => {
  const db = router.db;
  const { name, description, ended_at, outcomes } = req.body || {};

  if (!name || typeof name !== 'string' || !Array.isArray(outcomes) || outcomes.length === 0) {
    return res.status(422).json({ error: 'Validation failed' });
  }
  for (const o of outcomes) {
    if (!o || typeof o !== 'object' || typeof o.name !== 'string' || typeof o.coefficient !== 'number' || !isFinite(o.coefficient) || o.coefficient <= 0) {
      return res.status(422).json({ error: 'Validation failed: invalid outcome' });
    }
  }

  const nextEventId = (db.get('events').value().slice(-1)[0]?.id || 0) + 1;
  let nextOutcomeIdBase = 0;
  const allOutcomes = db.get('events').value().flatMap(e => e.outcomes || []);
  nextOutcomeIdBase = (allOutcomes.slice(-1)[0]?.id || 0) + 1;

  const eventToInsert = {
    id: nextEventId,
    author_id: req.user.id,
    name,
    description: description || '',
    ended_at,
    final_outcome_id: null,
    outcomes: outcomes.map((o, idx) => ({ id: nextOutcomeIdBase + idx, name: o.name, coefficient: o.coefficient }))
  };

  db.get('events').push(eventToInsert).write();

  return res.status(200).json({ event_id: nextEventId });
});

 

server.patch('/events/my/:id', authenticate, (req, res) => {
  const db = router.db;
  const eventId = parseInt(req.params.id);
  const event = db.get('events').find({ id: eventId }).value();

  if (!event) {
    return res.status(404).json({ error: 'Event not found' });
  }

  if (event.author_id && event.author_id !== req.user.id) {
    return res.status(403).json({ error: 'Forbidden: not an author' });
  }

  const { final_outcome_id, outcomes } = req.body || {};

  if (final_outcome_id === undefined && !Array.isArray(outcomes)) {
    return res.status(400).json({ error: 'Bad request' });
  }

  if (final_outcome_id !== undefined) {
    if (event.final_outcome_id !== null && event.final_outcome_id !== undefined) {
      return res.status(409).json({ error: 'Final outcome already set' });
    }

    if (final_outcome_id !== null) {
      const found = (event.outcomes || []).some(o => o.id === final_outcome_id);
      if (!found) {
        return res.status(404).json({ error: 'Outcome not found' });
      }
    }
  }

  if (Array.isArray(outcomes)) {
    for (const upd of outcomes) {
      if (upd == null || typeof upd !== 'object') {
        return res.status(400).json({ error: 'Bad request: outcomes format' });
      }
      const { outcome_id, coefficient } = upd;
      if (outcome_id === undefined || coefficient === undefined) {
        return res.status(400).json({ error: 'Bad request: outcome_id and coefficient required' });
      }
      const exists = (event.outcomes || []).some(o => o.id === outcome_id);
      if (!exists) {
        return res.status(404).json({ error: 'Outcome not found' });
      }
      if (typeof coefficient !== 'number' || !isFinite(coefficient) || coefficient <= 0) {
        return res.status(400).json({ error: 'Bad request: invalid coefficient' });
      }
    }

    db.get('events')
      .find({ id: eventId })
      .assign({
        outcomes: event.outcomes.map(o => {
          const upd = outcomes.find(u => u.outcome_id === o.id);
          return upd ? { ...o, coefficient: upd.coefficient } : o;
        })
      })
      .write();
  }

  if (final_outcome_id !== undefined) {
    db.get('events')
      .find({ id: eventId })
      .assign({ final_outcome_id })
      .write();
  }

  return res.status(200).json({ message: 'Event updated' });
});

 

server.post('/bets/my', authenticate, (req, res) => {
  const { event_id, outcome_id, size } = req.body || {};
  const db = router.db;
  
  if (event_id === undefined || outcome_id === undefined || size === undefined) {
    return res.status(400).json({ error: 'Bad request' });
  }
  
  const event = db.get('events').find({ id: event_id }).value();
  if (!event) {
    return res.status(404).json({ error: 'Event not found' });
  }
  
  const outcome = event.outcomes.find(o => o.id === outcome_id);
  if (!outcome) {
    return res.status(404).json({ error: 'Outcome not found' });
  }
  
  if (new Date(event.ended_at) <= new Date()) {
    return res.status(403).json({ error: 'Betting closed' });
  }
  
  if (req.user.balance < size) {
    return res.status(409).json({ error: 'Insufficient balance' });
  }
  
  db.get('users')
    .find({ id: req.user.id })
    .update('balance', balance => balance - size)
    .write();
  
  db.get('bets').push({
    id: db.get('bets').value().length + 1,
    user_id: req.user.id,
    event_id,
    outcome_id,
    size,
    amount: size,
    coefficient: outcome.coefficient,
    created_at: new Date().toISOString(),
    status: 'pending'
  }).write();
  
  res.status(200).json({ message: 'Bet placed successfully' });
});

 

 

server.get('/bets/my', authenticate, (req, res) => {
  const db = router.db;
  const items = db.get('bets')
    .filter({ user_id: req.user.id })
    .map(bet => {
      const event = db.get('events').find({ id: bet.event_id }).value();
      const outcomeName = event?.outcomes.find(o => o.id === bet.outcome_id)?.name || null;
      const finalOutcomeName = event?.final_outcome_id ? (event?.outcomes.find(o => o.id === event.final_outcome_id)?.name || null) : null;
      return {
        event_name: event?.name || 'Unknown Event',
        size: bet.size ?? bet.amount ?? 0,
        outcome_name: outcomeName,
        final_outcome_name: finalOutcomeName
      };
    })
    .value();
  res.status(200).json(items);
});

 

server.get('/bets/:event_id/:outcome_id', authenticate, (req, res) => {
  const db = router.db;
  const eventId = parseInt(req.params.event_id);
  const outcomeId = parseInt(req.params.outcome_id);

  const event = db.get('events').find({ id: eventId }).value();
  if (!event) return res.status(404).json({ error: 'Event not found' });
  const outcomeExists = (event.outcomes || []).some(o => o.id === outcomeId);
  if (!outcomeExists) return res.status(404).json({ error: 'Outcome not found' });

  const rows = db.get('bets')
    .filter({ event_id: eventId, outcome_id: outcomeId })
    .map(b => {
      const user = db.get('users').find({ id: b.user_id }).value();
      return { login: user?.login || 'unknown', size: b.size ?? b.amount ?? 0 };
    })
    .value();

  return res.status(200).json(rows);
});

 

server.use('/', router);

module.exports = server;

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`JSON Server is running on port ${PORT}`);
  console.log('Endpoints:');
  console.log(`- http://localhost:${PORT}/events/all`);
  console.log(`- http://localhost:${PORT}/events/{id}`);
  console.log(`- http://localhost:${PORT}/events/my/all`);
  console.log(`- http://localhost:${PORT}/bets/my`);
  console.log(`- http://localhost:${PORT}/auth/login`);
  console.log(`- http://localhost:${PORT}/user/balance`);
  console.log(`- http://localhost:${PORT}/user/info`);
  console.log('\nFrontend running at http://localhost:5173');
});
