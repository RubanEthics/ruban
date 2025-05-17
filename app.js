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

setQueues([new BullAdapter(libQueue)]);

app.use('/uploads', cors(), express.static(path.join(__dirname, 'uploads')));
app.use('/play-video-hls/', cors(), express.static(path.join(__dirname, 'uploads', 'hls')))
app.use('/play-video', cors(), express.static(path.join(__dirname, 'uploads', 'videos')));
app.use('/play-trailer', cors(), express.static(path.join(__dirname, 'uploads', 'trailers')));
app.use('/play-audio', cors(), express.static(path.join(__dirname, 'uploads', 'audios')));
app.use('/images', cors(), express.static(path.join(__dirname, 'uploads', 'images')));
app.use('/document', cors(), express.static(path.join(__dirname, 'uploads', 'documents')));
app.use('/public', cors(), express.static(path.join(__dirname, 'public')));


app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');

app.use(logger('dev'));
app.use(express.json());
app.use(cookieParser());

app.use(cors());

app.use(function (req, res, next) {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept','*');
    next();
});

app.use(express.urlencoded({ extended: false }));
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json())
cron.schedule('0 0 * * *', async () => {
    cronJobs()
});


app.use('/admin/videos', videoRoutes);
app.use('/api', require('./Controllers/CommonApiController'));
app.use('/queues', require('bull-board').router);

// Prefix 
app.use('/users', authRoutes); // User Route 
app.use('/partner', authPartnerRoutes); // User Route 
app.use('/admin', adminRoutes); // Admin Route
app.use('/Front-End', frontEndRoutes); // Front-End Route
app.use('/advertiser', advertiserRoutes); // Advertiser Route
app.use('/Multi-Profile', authenticateJWT, multiprofile); // MultiProfile ROUTE
app.use('/tv-login', TvRoute); // Admin Route

app.use((req, res, next) => {
    req.setTimeout(0); // no timeout
    res.setTimeout(0); // no timeout
    next();
});


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

// Import video worker script
require('./workers/libraryWorker');

app.get('/', (req, res) => {
    res.json({
        message: "Welcome to the Node API",
        node_version: process.version
    });
});

// The method below is used to avoid app crash issues.

process.on('unhandledRejection', (reason, promise) => {
    console.error('❌ Reason:', reason instanceof Error ? reason?.stack : reason);
});
process.on('uncaughtException', (err) => {
    console.error('Uncaught Exception:', err);
});

const port = process.env.PORT || 7006;
app.listen(port, () => {
    console.log(`🚀 Server running on ${process.env.BASE_URL}`);
});

module.exports = app;