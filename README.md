<div align="center">

# 🌍 Echoes of Earth

### Real-Time Global Crisis Visualization

An interactive 3D globe that transforms live news into dramatic terrain deformations — conflicts erupt as fiery spikes, economies sink into blue vortexes, disasters ripple as shockwave rings, and pandemics pulse as toxic green blisters.

**[Live Demo](#) · [Report Bug](../../issues) · [Request Feature](../../issues)**

![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=white)
![Three.js](https://img.shields.io/badge/Three.js-r182-000000?logo=threedotjs&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-7-646CFF?logo=vite&logoColor=white)
![Tailwind](https://img.shields.io/badge/Tailwind_CSS-4-06B6D4?logo=tailwindcss&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

</div>

---

## ✨ Features

- 🌐 **Interactive 3D Globe** — Powered by Three.js with custom GLSL shaders for real-time deformation
- 📰 **Live News Integration** — Fetches real-time crisis data from NewsAPI with smart fallback to mock data
- 🧠 **NLP Classification** — Multi-signal pipeline classifies articles into conflict, economic, disaster & health
- 🗺️ **96 Countries** — Automatic geolocation with country detection, aliases, and city-level mapping
- 📊 **Severity Scoring** — Weighted algorithm calculates crisis intensity per region
- 🔍 **Country Search** — Search & navigate to any country with smooth globe rotation animation
- 📅 **7-Day Timeline** — Slide through the past week's crisis data with per-day history
- 🎛️ **Crisis Filters** — Toggle crisis types on/off to focus your view
- 📊 **Statistics Panel** — Real-time metrics, breakdowns, and most-affected country tracking

### 🎨 4 Deformation Types

| Type | Visual | Description |
|------|--------|-------------|
| 🔴 **Conflict** | Sharp crystalline spikes | Fiery orange/red glow with pulsing animation |
| 🔵 **Economic** | Deep vortex funnels | Blue energy with concentric ring animation |
| 🟠 **Disaster** | Shockwave ripple rings | Amber concentric waves radiating from epicenter |
| 🟢 **Health** | Pulsating organic blisters | Toxic green domes with breathing animation |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | React 19 |
| **3D Rendering** | Three.js + React Three Fiber + Drei |
| **Shaders** | Custom GLSL (vertex displacement + fragment coloring) |
| **Styling** | Tailwind CSS v4 |
| **Animations** | Framer Motion + CSS Animations |
| **State Management** | React Context + useReducer |
| **News Data** | NewsAPI.org |
| **Build Tool** | Vite 7 |
| **Deployment** | Vercel (with serverless API proxy) |
| **E2E Testing** | Selenium + Pytest |

---

## 🚀 Getting Started

### Prerequisites

- [Node.js](https://nodejs.org/) v18 or higher
- [npm](https://www.npmjs.com/) v9 or higher
- A [NewsAPI](https://newsapi.org/) API key (free tier works for development)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/naitikk31/Echoes-of-Earth.git
   cd echoes-of-earth
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm run dev
   ```

4. **Open** [http://localhost:5173](http://localhost:5173) in your browser

---

## 🏗️ Architecture

```
src/
├── components/                 # React UI components
│   ├── Globe.jsx               # 3D globe with GLSL shaders & vertex deformation
│   ├── Overlay.jsx             # HUD layout compositor
│   ├── NewsPanel.jsx           # Country detail panel with articles
│   ├── SearchBar.jsx           # Country search with autocomplete
│   ├── StatsPanel.jsx          # Statistics dashboard
│   ├── CrisisFilter.jsx        # Crisis type toggle filters
│   ├── HistorySlider.jsx       # 7-day timeline navigator
│   ├── ControlBar.jsx          # Rotation & refresh controls
│   ├── CountryHighlight.jsx    # Country border glow effect
│   ├── Legend.jsx              # Crisis type legend
│   └── LoadingSpinner.jsx      # Loading overlay
├── services/
│   └── newsService.js          # NewsAPI fetcher with mock fallback
├── hooks/
│   └── useNewsData.js          # Data pipeline orchestrator
├── store/
│   └── newsStore.jsx           # Global state (Context + useReducer)
├── utils/
│   ├── crisisClassifier.js     # NLP crisis type classifier
│   ├── countryCoordinates.js   # Country database & geolocation
│   ├── countryBorders.js       # TopoJSON border rendering
│   └── severityCalculator.js   # Per-country severity scoring
├── App.jsx                     # Root component
└── App.css                     # All component styles
```

### Data Pipeline

```
NewsAPI → Fetch Articles → Classify (NLP) → Geolocate → Score Severity → Render on Globe
```

1. **Fetch** — Retrieves crisis-related news for each of the past 7 days (parallel fetching)
2. **Classify** — Multi-signal NLP with strong phrases, weighted keywords, and ambiguity filtering
3. **Geolocate** — Regex-based country detection with alias mapping (96 countries, 200+ aliases)
4. **Score** — Weighted severity calculation (article count × 0.6 + keyword weight × 0.4)
5. **Render** — Per-vertex GLSL displacement with type-specific deformation patterns on a 128×128 sphere

---

## 🌐 Deployment

### Deploy to Vercel (Recommended)

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/echoes-of-earth.git
   git push -u origin main
   ```

2. **Import to Vercel**
   - Go to [vercel.com](https://vercel.com) and click **"New Project"**
   - Import your GitHub repository

3. **Configure environment variables** in Vercel dashboard:
   | Variable | Value | Description |
   |----------|-------|-------------|
   | `NEWS_API_KEY` | `your_actual_api_key` | Server-side only — used by the serverless proxy |
   | `VITE_NEWS_API_KEY` | `proxy` | Tells the client to use the API proxy instead of mock data |

4. **Click Deploy** — Your app will be live at `your-project.vercel.app`

> [!IMPORTANT]
> The project includes a **serverless API proxy** (`api/proxy.js`) that keeps your API key secure by making NewsAPI requests server-side. This also solves CORS issues with NewsAPI's free plan.

### Build for Production

```bash
npm run build      # Generate production bundle in dist/
npm run preview    # Preview the production build locally
```

---

## 🧪 Testing

### E2E Tests (Selenium + Pytest)

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run all tests
pytest tests/ -v

# Run specific test suites
pytest tests/test_page_load.py -v      # Page load & initial render
pytest tests/test_search.py -v         # Search functionality
pytest tests/test_filter.py -v         # Crisis type filtering
pytest tests/test_responsiveness.py -v # Responsive design
```

Available test markers: `smoke`, `interaction`, `panel`, `search`, `filter`, `history`, `responsive`

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. **Fork** the repository
2. **Create** your feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙏 Acknowledgments

- [Three.js](https://threejs.org/) & [React Three Fiber](https://docs.pmnd.rs/react-three-fiber) — 3D rendering
- [NewsAPI](https://newsapi.org/) — Real-time news data
- [Natural Earth](https://www.naturalearthdata.com/) — Country border data via world-atlas
- [NASA Blue Marble](https://visibleearth.nasa.gov/) — Earth texture
- [Lucide](https://lucide.dev/) — Beautiful icon library
