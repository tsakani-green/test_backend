// api-helpers.js - Enhanced API integration helpers for EnvironmentalCategory

import { API_BASE_URL } from "../../config/api";

/**
 * Calculate carbon emissions from energy consumption
 * Formula: energy (kWh) * 0.99 / 1000 = carbon (tCO₂e)
 */
export const calculateCarbonFromEnergy = (energyKwh) => {
  if (!energyKwh || isNaN(energyKwh)) return 0;
  return (energyKwh * 0.99) / 1000;
};

/**
 * Fetch ESG data from backend
 * Returns: { mockData, insights, uploaded_date }
 */
export const fetchESGData = async () => {
  try {
    console.log("📊 Fetching ESG data from API...");
    
    let response = await fetch(`${API_BASE_URL}/api/esg-data`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });

    // If GET returns 405, try POST
    if (response.status === 405) {
      console.log("⚠️ GET not allowed, trying POST...");
      response = await fetch(`${API_BASE_URL}/api/esg-data`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({}),
      });
    }

    if (!response.ok) {
      const errorText = await response.text();
      console.warn(`❌ Failed to fetch ESG data: ${response.status} - ${errorText}`);
      return null;
    }

    const data = await response.json();
    console.log("✅ ESG data fetched successfully:", data);
    return data;
  } catch (error) {
    console.error("❌ Error fetching ESG data:", error);
    return null;
  }
};

/**
 * Fetch invoices with pagination and search
 * Parameters:
 * - q: search query string
 * - company: filter by company name
 * - page: page number (1-based)
 * - page_size: items per page
 * - sort: "invoice_date_desc" | "invoice_date_asc" | "updated_at_desc" | "updated_at_asc"
 */
export const fetchInvoiceQuery = async (params) => {
  try {
    const url = new URL(`${API_BASE_URL}/api/invoices/query`);
    
    Object.entries(params).forEach(([k, v]) => {
      if (v === null || v === undefined) return;
      if (typeof v === "string" && v.trim() === "") return;
      url.searchParams.set(k, String(v));
    });
    
    console.log("📋 Fetching invoice query:", url.toString());
    const res = await fetch(url.toString(), { method: "GET" });
    
    if (!res.ok) {
      throw new Error(`Failed to query invoices (${res.status})`);
    }
    
    const data = await res.json();
    console.log("✅ Invoice query successful:", data);
    return data;
  } catch (error) {
    console.error("❌ Error fetching invoice query:", error);
    throw error;
  }
};

/**
 * Fetch environmental insights from invoices
 * last_n: number of invoices to analyze (default: 6)
 */
export const fetchInvoiceEnvironmentalInsights = async (last_n = 6) => {
  try {
    const url = new URL(`${API_BASE_URL}/api/invoice-environmental-insights`);
    url.searchParams.set("last_n", String(last_n));
    
    console.log("🌱 Fetching invoice environmental insights...");
    const res = await fetch(url.toString(), { method: "GET" });
    
    if (!res.ok) {
      throw new Error(`Failed to fetch insights (${res.status})`);
    }
    
    const data = await res.json();
    console.log("✅ Environmental insights fetched:", data);
    return data;
  } catch (error) {
    console.error("❌ Error fetching environmental insights:", error);
    throw error;
  }
};

/**
 * Post environmental insights request
 * Generates AI-powered insights based on metrics
 */
export const postEnvironmentalInsights = async (payload) => {
  try {
    console.log("🤖 Generating environmental insights...", payload);
    
    const res = await fetch(`${API_BASE_URL}/api/environmental-insights`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    
    if (!res.ok) {
      throw new Error(`Failed to generate insights (${res.status})`);
    }
    
    const data = await res.json();
    console.log("✅ Insights generated successfully:", data);
    return data;
  } catch (error) {
    console.error("❌ Error generating environmental insights:", error);
    throw error;
  }
};

/**
 * Save invoices to MongoDB
 * Persists invoice data to database
 */
export const saveInvoicesToMongoDB = async (invoiceData) => {
  try {
    // Ensure invoiceData is an array
    if (!Array.isArray(invoiceData)) {
      console.warn("⚠️ invoiceData is not an array, attempting to convert...");
      
      if (invoiceData && typeof invoiceData === "object") {
        if (invoiceData.data && Array.isArray(invoiceData.data)) {
          invoiceData = invoiceData.data;
        } else if (invoiceData.invoices && Array.isArray(invoiceData.invoices)) {
          invoiceData = invoiceData.invoices;
        } else if (Object.keys(invoiceData).every(key => !isNaN(key))) {
          invoiceData = Object.values(invoiceData);
        } else {
          invoiceData = [invoiceData];
        }
      } else {
        throw new Error("invoiceData must be an array or object");
      }
    }

    console.log("💾 Saving", invoiceData.length, "invoices to MongoDB...");
    
    // Clean up the data before sending
    const cleanedData = invoiceData.map(invoice => {
      const cleanInvoice = { ...invoice };
      
      // Ensure carbon is calculated if not present
      if (!cleanInvoice.estimated_carbon_tonnes && cleanInvoice.total_energy_kwh) {
        cleanInvoice.estimated_carbon_tonnes = calculateCarbonFromEnergy(
          cleanInvoice.total_energy_kwh
        );
      }
      
      // Remove undefined/null values
      Object.keys(cleanInvoice).forEach(key => {
        if (cleanInvoice[key] === undefined || cleanInvoice[key] === null) {
          delete cleanInvoice[key];
        }
      });
      
      return cleanInvoice;
    });

    const response = await fetch(`${API_BASE_URL}/api/invoices/save-to-mongodb`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        invoices: cleanedData,
        mongoDbName: "esg_app",
        timestamp: new Date().toISOString()
      }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error("❌ MongoDB save error:", errorText);
      throw new Error(`Failed to save to MongoDB: ${response.status}`);
    }

    const result = await response.json();
    console.log("✅ Successfully saved to MongoDB:", result);
    return result;
  } catch (error) {
    console.error("❌ Error saving to MongoDB:", error);
    throw error;
  }
};

/**
 * Load invoices from MongoDB
 * Retrieves all stored invoices from database
 */
export const loadInvoicesFromMongoDB = async () => {
  try {
    console.log("📂 Loading invoices from MongoDB...");
    
    const response = await fetch(`${API_BASE_URL}/api/invoices/load-from-mongodb`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Failed to load from MongoDB: ${response.status}`);
    }

    const result = await response.json();
    console.log("✅ Invoices loaded from MongoDB:", result);
    
    // Handle different response formats
    if (Array.isArray(result)) {
      return { invoices: result, count: result.length };
    } else if (result && Array.isArray(result.invoices)) {
      return result;
    } else if (result && Array.isArray(result.data)) {
      return { invoices: result.data, count: result.data.length };
    } else {
      console.warn("⚠️ Unexpected response format:", result);
      return { invoices: [], count: 0 };
    }
  } catch (error) {
    console.error("❌ Error loading from MongoDB:", error);
    throw error;
  }
};

/**
 * Get MongoDB statistics
 * Returns database stats and aggregated metrics
 */
export const getMongoDBStats = async () => {
  try {
    console.log("📊 Fetching MongoDB statistics...");
    
    const response = await fetch(`${API_BASE_URL}/api/invoices/mongodb-stats`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });

    if (!response.ok) {
      throw new Error(`Failed to get stats: ${response.status}`);
    }

    const stats = await response.json();
    console.log("✅ MongoDB stats retrieved:", stats);
    return stats;
  } catch (error) {
    console.error("❌ Error fetching MongoDB stats:", error);
    throw error;
  }
};

/**
 * Setup WebSocket connection for live updates
 * Automatically reconnects on disconnect
 */
export const setupWebSocket = (wsUrl, onUpdate, onError) => {
  try {
    const ws = new WebSocket(wsUrl);
    
    ws.onopen = () => {
      console.log("✅ WebSocket connected");
      ws.send("ping");
    };
    
    ws.onclose = () => {
      console.log("⚠️ WebSocket disconnected");
      // Attempt to reconnect after 3 seconds
      setTimeout(() => {
        console.log("🔄 Attempting to reconnect WebSocket...");
        setupWebSocket(wsUrl, onUpdate, onError);
      }, 3000);
    };
    
    ws.onerror = (error) => {
      console.error("❌ WebSocket error:", error);
      if (onError) onError(error);
    };
    
    ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data);
        if (msg?.type === "live-esg-update") {
          console.log("📡 WebSocket update received:", msg);
          if (onUpdate) onUpdate(msg.data);
        }
      } catch {
        // Ignore non-JSON messages
      }
    };
    
    return ws;
  } catch (error) {
    console.error("❌ Failed to setup WebSocket:", error);
    if (onError) onError(error);
    return null;
  }
};

/**
 * Upload PDF invoices to backend
 * Backend extracts data and returns invoice summaries
 */
export const uploadInvoiceFiles = async (files) => {
  try {
    if (!files || files.length === 0) {
      throw new Error("No files selected");
    }

    const formData = new FormData();
    
    // Handle single file or multiple files
    if (files instanceof FileList) {
      for (let i = 0; i < files.length; i++) {
        formData.append("files", files[i]);
      }
    } else if (Array.isArray(files)) {
      files.forEach((file, index) => {
        formData.append("files", file);
      });
    } else {
      formData.append("files", files);
    }

    console.log("📤 Uploading", files.length, "invoice files...");
    
    const response = await fetch(`${API_BASE_URL}/api/invoice-bulk-upload`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Upload failed: ${response.status}`);
    }

    const result = await response.json();
    console.log("✅ Invoice files uploaded successfully:", result);
    return result;
  } catch (error) {
    console.error("❌ Error uploading invoices:", error);
    throw error;
  }
};

// Export all helpers
export default {
  calculateCarbonFromEnergy,
  fetchESGData,
  fetchInvoiceQuery,
  fetchInvoiceEnvironmentalInsights,
  postEnvironmentalInsights,
  saveInvoicesToMongoDB,
  loadInvoicesFromMongoDB,
  getMongoDBStats,
  setupWebSocket,
  uploadInvoiceFiles,
};
