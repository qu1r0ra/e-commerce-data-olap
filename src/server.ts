import express from 'express';
import cors from 'cors';
import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv'; //my .env locally is in root folder

dotenv.config();

const app = express();
const port = 3001; // port to run on

app.use(cors());
app.use(express.json());


const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_KEY;

// just crash the app if the keys r missing
if (!supabaseUrl || !supabaseKey) {
  throw new Error('Supabase URL and key must be provided in .env file');
}
const supabase = createClient(supabaseUrl, supabaseKey);


app.get('/api/etl-status', async (req, res) => {
  console.log("Request received for /api/etl-status");
  try {
    // SUPABASE QUERY FOR ETL STATS
    const { data, error } = await supabase
      .from('ETLControl')
      .select('tableName, lastLoadTime');

    /*
      SELECT "tableName", "lastLoadTime" FROM "ETLControl";
    */

    if (error) throw error;

    // the data comes back as an array like: [{tableName: 'DimUsers', lastLoadTime: '...'}, ...].
    // we use .reduce() to turn it into a single object like: { DimUsers: '...', DimProducts: '...' }.
    // just frontend convenience
    const etlStatus = data.reduce((acc, record) => {
      acc[record.tableName] = record.lastLoadTime;
      return acc;
    }, {} as Record<string, string>);

    res.json(etlStatus);
  } catch (error) {
    console.error('Error fetching ETL status:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});


//
app.get('/api/sales-rollup', async (req, res) => {
  // we get the groupby value from the query string, if it's not provided, we default to 'month'.
  const { groupBy = 'month' } = req.query;

  const groupByColumns: Record<string, string> = {
    day: 'fullDate', month: 'monthName', year: 'year', quarter: 'quarter'
  };
  const dateColumn = groupByColumns[groupBy as string] || 'monthName';

  try {
    //our rollup query
    const { data, error } = await supabase
      .from('FactSales')
      .select(`quantitySold, DimProducts ( price ), DimDate ( ${dateColumn}, year, month )`)
      .order('year', { foreignTable: 'DimDate', ascending: true })
      .order('month', { foreignTable: 'DimDate', ascending: true });
    /*
      SELECT
        fs."quantitySold",
        dp.price,
        dd."monthName",
        dd.year,
        dd.month
      FROM "FactSales" fs
      JOIN "DimProducts" dp ON fs."productId" = dp.id
      JOIN "DimDate" dd ON fs."deliveryDateId" = dd.id
      ORDER BY dd.year, dd.month;
    */

    if (error) throw error;

    // loop through every sale record
    const salesByPeriod = data.reduce((acc, sale) => {
      const period = sale.DimDate?.[dateColumn] || 'Unknown';
      const revenue = (sale.quantitySold || 0) * (sale.DimProducts?.price || 0);
      // calculate the revenue for this one sale ^^

      // and add it up here. If we haven't seen this period before, start it at 0.
      if (!acc[period]) {
        acc[period] = 0;
      }
      acc[period] += revenue; // then add this sale's revenue to the total for that period.
      return acc;
    }, {} as Record<string, number>);

    res.json(salesByPeriod);
  } catch (error) {
    console.error('Error fetching sales roll-up data:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});


// 
app.get('/api/sales-by-category', async (req, res) => {
  try {
    const { data, error } = await supabase
      .from('FactSales')
      .select('quantitySold, DimProducts ( category, price )');

    /*
      Equivalent SQL Statement:
      SELECT
        fs."quantitySold",
        dp.category,
        dp.price
      FROM "FactSales" fs
      JOIN "DimProducts" dp ON fs."productId" = dp.id;
    */

    if (error) throw error;

    const salesByCategory = data.reduce((acc, sale) => {
      const category = sale.DimProducts?.category || 'Unknown';
      const revenue = (sale.quantitySold || 0) * (sale.DimProducts?.price || 0);
      if (!acc[category]) acc[category] = 0;
      acc[category] += revenue;
      return acc;
    }, {} as Record<string, number>);

    res.json(salesByCategory);
  } catch (error) {
    console.error('Error fetching sales by category:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});


// 
app.get('/api/sales-by-product', async (req, res) => {
  const { category } = req.query;

  if (!category) {
    return res.status(400).json({ error: 'Category query parameter is required' });
  }

  try {
    const { data, error } = await supabase
      .from('FactSales')
      .select('quantitySold, DimProducts!inner( name, price, category )')
      .eq('DimProducts.category', category as string);

    /*
      Equivalent SQL Statement (example for 'Electronics'):
      SELECT
        fs."quantitySold",
        dp.name,
        dp.price,
        dp.category
      FROM "FactSales" fs
      INNER JOIN "DimProducts" dp ON fs."productId" = dp.id
      WHERE dp.category = 'Electronics';
    */

    if (error) throw error;

    const salesByProduct = data.reduce((acc, sale) => {
      const productName = sale.DimProducts?.name || 'Unknown';
      const revenue = (sale.quantitySold || 0) * (sale.DimProducts?.price || 0);
      if (!acc[productName]) acc[productName] = 0;
      acc[productName] += revenue;
      return acc;
    }, {} as Record<string, number>);

    res.json(salesByProduct);
  } catch (error) {
    console.error(`Error fetching sales by product for category "${category}":`, error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});


app.get('/api/rider-demographics', async (req, res) => {
  const { query, courierName } = req.query;

  try {
    if (query === 'couriers') {
      const { data, error } = await supabase.from('DimRiders').select('courierName');
      // SELECT "courierName" FROM "DimRiders";

      if (error) throw error;
      // The data might have duplicates (e.g., Grab, Grab, Lalamove).
      // new set is a trick to get only the unique values.
      const uniqueCouriers = [...new Set(data.map(r => r.courierName).filter(Boolean))].sort();
      return res.json(uniqueCouriers);
    }

    let queryBuilder = supabase.from('DimRiders').select('vehicleType, gender');

    // If a courierName was provided in the URL, we add a .eq() filter (like a WHERE clause).
    if (courierName) {
      queryBuilder = queryBuilder.eq('courierName', courierName as string);
    }

    /*
      SQL if courierName is Grab:
      SELECT "vehicleType", "gender" FROM "DimRiders" WHERE "courierName" = 'Grab';

      SQL if none
      SELECT "vehicleType", "gender" FROM "DimRiders";
    */

    const { data, error } = await queryBuilder;
    if (error) throw error;

    // create combined keys like "Motorcycle (Male)".
    const ridersByGroup = data.reduce((acc, rider) => {
      const vehicle = rider.vehicleType || 'Unknown Vehicle';
      const gender = rider.gender || 'Unknown Gender';
      const key = `${vehicle} (${gender})`;

      if (!acc[key]) acc[key] = 0;
      acc[key] += 1; //count riders
      return acc;
    }, {} as Record<string, number>);

    res.json(ridersByGroup);

  } catch (error) {
    console.error('Error fetching rider demographics:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});


// -- START THE SERVER --
// This command tells our app to start listening for requests on the port we defined.
app.listen(port, () => {
  console.log(`Backend server listening at http://localhost:${port}`);
});