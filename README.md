# 🌍 AfricaESG.AI - Environmental Dashboard with Database Integration

A comprehensive ESG (Environmental, Social, Governance) tracking platform with PDF invoice processing, real-time data persistence, and AI-powered environmental insights.

## ✨ Features

### 📊 Environmental Tracking
- ✅ Energy consumption monitoring (kWh)
- ✅ Water usage tracking (m³) - **NEW**
- ✅ Water cost analysis (R) - **NEW**
- ✅ Carbon emissions calculation (tCO₂e)
- ✅ Monthly trend analysis
- ✅ Company-wise performance comparison

### 📄 Invoice Processing
- ✅ PDF invoice upload (bulk)
- ✅ Automatic data extraction
- ✅ Energy and water data parsing
- ✅ Invoice history management
- ✅ Tax invoice tracking
- ✅ Multi-company support

### 💾 Database Integration
- ✅ MongoDB data persistence
- ✅ Automatic data upsert
- ✅ Query with pagination
- ✅ Search and filter
- ✅ Database statistics
- ✅ Fallback to in-memory storage

### 🤖 AI Features
- ✅ Environmental insights generation
- ✅ Water conservation recommendations
- ✅ Energy efficiency analysis
- ✅ Carbon reduction strategies
- ✅ ESG performance scoring

### 🔄 Real-time Updates
- ✅ WebSocket live connections
- ✅ Auto-refresh on data changes
- ✅ Multi-client broadcasting
- ✅ Connection status indicator
- ✅ Debounced updates (250ms)

### 📈 Visualizations
- ✅ Energy consumption charts
- ✅ Carbon emissions trends
- ✅ Water usage analysis
- ✅ Performance radar charts
- ✅ Monthly breakdowns
- ✅ Company comparisons

### 📋 Data Management
- ✅ Invoice table with all metrics
- ✅ Water data in all tables
- ✅ Detail modal views
- ✅ Export capabilities (CSV, PDF)
- ✅ Search functionality
- ✅ Sort and filter options

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│         React Frontend (EnvironmentalCategory)       │
│  - Data visualization                               │
│  - Invoice upload/management                        │
│  - Real-time UI updates                             │
└─────────────────────────────────────────────────────┘
                        │
         ┌──────────────┼──────────────┐
         │              │              │
    REST API        WebSocket      File Upload
    (HTTP)          (ws://)         (PDF)
         │              │              │
         └──────────────┼──────────────┘
                        │
┌─────────────────────────────────────────────────────┐
│     FastAPI Backend (main.py)                       │
│  - Invoice extraction                               │
│  - AI insight generation                            │
│  - Database operations                              │
│  - Real-time broadcasting                           │
└─────────────────────────────────────────────────────┘
                        │
┌─────────────────────────────────────────────────────┐
│     MongoDB Database                                │
│  - Invoices collection                              │
│  - Energy/water metrics                             │
│  - User data                                        │
│  - ESG records                                      │
└─────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 14+
- MongoDB (cloud or self-hosted)
- OpenAI API key (optional, for AI features)

### Backend Setup
```bash
# Navigate to project directory
cd c:\Workspace\mongoBD

# Install Python dependencies
pip install -r requirements.txt

# Set environment variables
export MONGODB_URI="mongodb+srv://..."
export OPENAI_API_KEY="sk-..."

# Run backend
python -m uvicorn main:app --reload --port 3001
```

### Frontend Setup
```bash
# In your React app directory
npm install

# Set API base URL
export REACT_APP_API_BASE_URL=http://localhost:3001

# Start React dev server
npm start
```

### Verify Setup
```bash
# Health check
curl http://localhost:3001/health

# Database status
curl http://localhost:3001/api/invoices/mongodb-stats

# API docs
open http://localhost:3001/docs
```

## 📖 Documentation

- **[Quick Start Guide](./QUICK_START.md)** - 5-minute setup guide
- **[Database Integration Guide](./DATABASE_INTEGRATION_GUIDE.md)** - Complete integration overview
- **[Implementation Guide](./IMPLEMENTATION_GUIDE.md)** - Step-by-step details
- **[React Integration Examples](./REACT_INTEGRATION_EXAMPLES.md)** - Code examples
- **[Integration Summary](./INTEGRATION_SUMMARY.md)** - What was implemented

## 🔧 API Endpoints

### ESG Data
- `GET /api/esg-data` - Get ESG metrics with uploaded invoices
- `POST /api/environmental-insights` - Generate environmental insights
- `POST /api/social-insights` - Generate social insights
- `POST /api/governance-insights` - Generate governance insights
- `POST /api/ai-mini-report` - Generate mini ESG report

### Invoices
- `GET /api/invoices` - Get all invoices (simple list)
- `GET /api/invoices/query` - Query invoices (paginated, searchable)
- `POST /api/invoice-upload` - Upload single PDF invoice
- `POST /api/invoice-bulk-upload` - Upload multiple PDF invoices
- `GET /api/invoice-environmental-insights` - Get invoice-based metrics

### Database Operations ✨
- `POST /api/invoices/save-to-mongodb` - Save invoices to database
- `GET /api/invoices/load-from-mongodb` - Load invoices from database
- `GET /api/invoices/mongodb-stats` - Get database statistics

### Real-time
- `WS /ws/live-ai` - WebSocket for live updates

### System
- `GET /health` - Health check
- `GET /` - Root endpoint
- `POST /auth/login` - User login
- `GET /auth/me` - Current user info

## 📊 Data Models

### Invoice
```javascript
{
  filename: string,
  company_name: string,
  invoice_date: string,
  tax_invoice_number: string,
  total_energy_kwh: number,
  water_usage: number,          // ✨ NEW
  water_cost: number,           // ✨ NEW
  total_current_charges: number,
  sixMonthHistory: [
    {
      month_label: string,
      energyKWh: number,
      water_m3: number,         // ✨ NEW
      water_cost: number,       // ✨ NEW
      carbonTco2e: number,
      total_current_charges: number
    }
  ]
}
```

### ESG Data
```javascript
{
  mockData: {
    summary: { ... },
    metrics: { ... },
    environmentalMetrics: {
      uploadedInvoiceData: [ ... ],
      aggregatedMetrics: {
        totalEnergyKwh: number,
        totalWaterM3: number,     // ✨ NEW
        estimatedCo2Tonnes: number,
        totalChargesRand: number
      }
    }
  },
  insights: [ string ],
  uploaded_date: string
}
```

## 🎯 Key Features Explained

### Water Data Integration ✨
Water usage is now tracked at multiple levels:
- **Invoice level**: Total water usage and cost
- **Monthly level**: Breakdown by month
- **Aggregated level**: Total across all invoices
- **Calculated metrics**: Water efficiency, water cost per kWh
- **Insights**: Conservation recommendations

### Carbon Calculation
Consistent formula throughout the system:
```
Carbon (tCO₂e) = Energy (kWh) × 0.99 / 1000
```

Applied at:
- Invoice level
- Monthly level
- Aggregated level
- Chart visualizations

### Real-time Updates
WebSocket broadcasts trigger automatic data refresh:
1. PDF uploaded → Backend extracts
2. Data saved to MongoDB → Broadcast to WebSocket clients
3. All connected clients receive update
4. UI refreshes automatically
5. Charts update with new data

### Database Persistence
- MongoDB stores all invoices
- Automatic upsert (no duplicates)
- Fallback to in-memory if DB unavailable
- Full text search support
- Pagination and filtering

## 🔐 Security

- ✅ CORS enabled for frontend
- ✅ Input validation (Pydantic models)
- ✅ MongoDB injection protection
- ✅ WebSocket validation
- 🔜 API authentication (JWT)
- 🔜 Rate limiting
- 🔜 Database encryption

## 📈 Performance

- **Parallel API calls**: 3 concurrent requests on load
- **Debounced updates**: 250ms debounce for WebSocket
- **Memoized calculations**: Prevents unnecessary re-renders
- **Pagination**: 25 items per page default
- **Lazy loading**: Charts render on-demand

## 🐛 Troubleshooting

### MongoDB Not Connecting
```bash
# Check status
curl http://localhost:3001/api/invoices/mongodb-stats

# Verify connection string
echo $MONGODB_URI
```

### WebSocket Issues
1. Open browser DevTools (F12)
2. Check Network → WS tab
3. Look for `/ws/live-ai` connection
4. Verify backend is running

### PDF Extraction Failing
- Ensure PDF has standard text layout
- Check for scanned images (use OCR if needed)
- Verify expected fields: energy, water, cost

### No Water Data
- PDF must contain water usage information
- Check invoice details modal for extraction results
- Verify field names match extraction logic

## 📝 Example Usage

### 1. Upload Invoice
```javascript
// Frontend
const files = [pdfFile];
await handleBulkInvoiceUpload(files);
// → Data automatically extracted and saved
```

### 2. Query Invoices
```javascript
const result = await fetchInvoiceQuery({
  q: "company name",
  company: "ABC Corp",
  page: 1,
  page_size: 25,
  sort: "invoice_date_desc"
});
```

### 3. Get Environmental Insights
```javascript
const insights = await postEnvironmentalInsights({
  company_name: "ABC Corp",
  period: "2024-Q1",
  metrics: { ... }
});
```

### 4. Save to Database
```javascript
const result = await saveInvoicesToMongoDB(invoiceSummaries);
if (result.success) {
  console.log(`Saved ${result.count} invoices`);
}
```

## 🎓 Learning Resources

- FastAPI docs: https://fastapi.tiangolo.com/
- MongoDB docs: https://docs.mongodb.com/
- React hooks: https://react.dev/reference/react/hooks
- WebSocket API: https://developer.mozilla.org/en-US/docs/Web/API/WebSocket

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- [ ] Mobile responsive design
- [ ] Dark mode support
- [ ] Custom reporting
- [ ] Benchmarking features
- [ ] Data export to Excel
- [ ] Multi-language support
- [ ] Advanced analytics
- [ ] Machine learning predictions

## 📄 License

MIT License - See LICENSE file for details

## 👥 Authors

- **GreenBDG Africa** - ESG Platform
- **Development Team** - Backend & Frontend

## 📞 Support

For issues or questions:
1. Check documentation files
2. Review error logs in browser console
3. Check backend logs in terminal
4. Verify MongoDB connection
5. Open GitHub issue

## 🗺️ Roadmap

### V2.0 (Q2 2024)
- [ ] Custom KPI definitions
- [ ] Benchmarking vs peers
- [ ] Advanced filtering
- [ ] Data backup/restore

### V3.0 (Q3 2024)
- [ ] Mobile app
- [ ] Automated alerts
- [ ] Predictive analytics
- [ ] Custom reports

### V4.0 (Q4 2024)
- [ ] Sustainability goals tracking
- [ ] Supply chain integration
- [ ] Third-party data connectors
- [ ] API for enterprise clients

---

**Status**: ✅ Production Ready (v2.1.0)

Last Updated: January 2024
