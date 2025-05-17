const createError = require('http-errors');
const express = require('express');
const path = require('path');
const dotenv = require('dotenv');
const logger = require('morgan');
const cookieParser = require('cookie-parser');
const bodyParser = require('body-parser');
const cors = require('cors');
const authRoutes = require('./Controllers/AuthController');
const authPartnerRoutes = require('./routes/partnerRoutes');
const videoRoutes = require('./routes/videoRoutes');
const frontEndRoutes = require('./routes/frontEndRoutes');
const advertiserRoutes = require('./routes/advertiserRoutes');
const { BullAdapter, setQueues } = require('bull-board');

const libQueue = require('./workers/libraryWorker');

const adminRoutes = require('./routes/adminRoutes');
const multiprofile = require('./routes/MultiProfileRoute');
const { authenticateJWT } = require('./middleware/AuthenticateMiddleware');
const cron = require('node-cron');
const cronJobs = require('./config/cronqueue.js');
const TvRoute = require('./routes/TvRoute');

dotenv.config();
const app = express();

// ✅ CORS CONFIGURATION
const allowedOrigins = [
  'http://localhost:3000',
  'https://admin-tcc.flicknexs.com'
];

const corsOptions = {
  origin: function (origin, callback) {
    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  optionsSuccessStatus: 200
};

app.use(cors(corsOptions));

setQueues([new BullAdapter(libQueue)]);

// Static Files with CORS
app.use('/uploads', express.static(path.join(__dirname, 'uploads')));
app.use('/play-video-hls/', express.static(path.join(__dirname, 'uploads', 'hls')));
app.use('/play-video', express.static(path.join(__dirname, 'uploads', 'videos')));
app.use('/play-trailer', express.static(path.join(__dirname, 'uploads', 'trailers')));
app.use('/play-audio', express.static(path.join(__dirname, 'uploads', 'audios')));
app.use('/images', express.static(path.join(__dirname, 'uploads', 'images')));
app.use('/document', express.static(path.join(__dirname, 'uploads', 'documents')));
app.use('/public', express.static(path.join(__dirname, 'public')));

app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');

app.use(logger('dev'));
app.use(express.json());
app.use(cookieParser());
app.use(express.urlencoded({ extended: false }));
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// Cron Job
cron.schedule('0 0 * * *', async () => {
  cronJobs();
});

// Routes
app.use('/admin/videos', videoRoutes);
app.use('/api', require('./Controllers/CommonApiController'));
app.use('/queues', require('bull-board').router);
app.use('/users', authRoutes); // User Route 
app.use('/partner', authPartnerRoutes); // Partner Route 
app.use('/admin', adminRoutes); // Admin Route
app.use('/Front-End', frontEndRoutes); // Front-End Route
app.use('/advertiser', advertiserRoutes); // Advertiser Route
app.use('/Multi-Profile', authenticateJWT, multiprofile); // MultiProfile Route
app.use('/tv-login', TvRoute); // TV Login Route

// Prevent Timeout
app.use((req, res, next) => {
  req.setTimeout(0);
  res.setTimeout(0);
  next();
});

// Error Handling
app.use((err, req, res, next) => {
  console.error('Error occurred:', err);
  next(createError(404));
});

app.use((err, req, res, next) => {
  console.error('Error occurred:', err);
  if (req.headers['accept'] && req.headers['accept'].includes('application/json')) {
    return res.status(500).json({
      status: false,
      status_code: 500,
      message: "Internal Server Error",
      error: err.message || 'Unknown error'
    });
  } else {
    res.locals.message = err.message;
    res.locals.error = req.app.get('env') === 'development' ? err : {};

    return res.status(500).json({
      status: false,
      status_code: 500,
      message: "Internal Server Error",
      error: err.message
    });
  }
});

// Worker
require('./workers/libraryWorker');

// Welcome Route
app.get('/', (req, res) => {
  res.json({
    message: "Welcome to the Node API",
    node_version: process.version
  });
});

// Handle Crashes
process.on('unhandledRejection', (reason, promise) => {
  console.error('❌ Reason:', reason instanceof Error ? reason?.stack : reason);
});

process.on('uncaughtException', (err) => {
  console.error('Uncaught Exception:', err);
});

// Server
const port = process.env.PORT || 7006;
app.listen(port, () => {
  console.log(`🚀 Server running on ${process.env.BASE_URL}`);
});

module.exports = app;
