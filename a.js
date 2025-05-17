const createError = require('http-errors');
const express = require('express');
const path = require('path');
const dotenv = require('dotenv');
const logger = require('morgan');
const cookieParser = require('cookie-parser');
const bodyParser = require('body-parser');
const cors = require('cors');
const { BullAdapter, setQueues } = require('bull-board');
const cron = require('node-cron');

// Load routes
const authRoutes = require('./Controllers/AuthController');
const authPartnerRoutes = require('./routes/partnerRoutes');
const videoRoutes = require('./routes/videoRoutes');
const frontEndRoutes = require('./routes/frontEndRoutes');
const advertiserRoutes = require('./routes/advertiserRoutes');
const adminRoutes = require('./routes/adminRoutes');
const multiprofile = require('./routes/MultiProfileRoute');
const TvRoute = require('./routes/TvRoute');

// Load middleware
const { authenticateJWT } = require('./middleware/AuthenticateMiddleware');
const cronJobs = require('./config/cronqueue.js');

// Load workers
const libQueue = require('./workers/libraryWorker');

dotenv.config();
const app = express();

// ✅ UNIVERSAL CORS SETUP
app.use(cors({
  origin: true, // Reflects request origin
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  optionsSuccessStatus: 200
}));

// ✅ Handle preflight requests
app.options('*', cors());

// Bull Queue
setQueues([new BullAdapter(libQueue)]);

// Static routes
app.use('/uploads', express.static(path.join(__dirname, 'uploads')));
app.use('/play-video-hls/', express.static(path.join(__dirname, 'uploads', 'hls')));
app.use('/play-video', express.static(path.join(__dirname, 'uploads', 'videos')));
app.use('/play-trailer', express.static(path.join(__dirname, 'uploads', 'trailers')));
app.use('/play-audio', express.static(path.join(__dirname, 'uploads', 'audios')));
app.use('/images', express.static(path.join(__dirname, 'uploads', 'images')));
app.use('/document', express.static(path.join(__dirname, 'uploads', 'documents')));
app.use('/public', express.static(path.join(__dirname, 'public')));

// View engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');

// Middleware setup
app.use(logger('dev'));
app.use(express.json());
app.use(cookieParser());
app.use(express.urlencoded({ extended: false }));
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// Cron jobs
cron.schedule('0 0 * * *', async () => {
    cronJobs();
});

// Routes
app.use('/admin/videos', videoRoutes);
app.use('/api', require('./Controllers/CommonApiController'));
app.use('/queues', require('bull-board').router);
app.use('/users', authRoutes);
app.use('/partner', authPartnerRoutes);
app.use('/admin', adminRoutes);
app.use('/Front-End', frontEndRoutes);
app.use('/advertiser', advertiserRoutes);
app.use('/Multi-Profile', authenticateJWT, multiprofile);
app.use('/tv-login', TvRoute);

// No timeout
app.use((req, res, next) => {
    req.setTimeout(0);
    res.setTimeout(0);
    next();
});

// Error handling
app.use((req, res, next) => {
    next(createError(404));
});

app.use((err, req, res, next) => {
    console.error('Error occurred:', err);
    if (req.headers['accept']?.includes('application/json')) {
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

// Root route
app.get('/', (req, res) => {
    res.json({
        message: "Welcome to the Node API",
        node_version: process.version
    });
});

// Global error catches
process.on('unhandledRejection', (reason) => {
    console.error('❌ Reason:', reason instanceof Error ? reason.stack : reason);
});
process.on('uncaughtException', (err) => {
    console.error('Uncaught Exception:', err);
});

// Start server
const port = process.env.PORT || 7006;
app.listen(port, () => {
    console.log(`🚀 Server running on ${process.env.BASE_URL || `http://localhost:${port}`}`);
});

module.exports = app;
