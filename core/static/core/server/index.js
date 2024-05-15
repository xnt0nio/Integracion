import express from "express";
import cors from "cors";
import { MercadoPagoConfig, Preference } from 'mercadopago';

// Configura las credenciales de Mercado Pago
const client = new MercadoPagoConfig({ accessToken: 'TEST-7400591541742198-050923-6fedd8b527f928b3112f0b3b4ae84957-1451079063' });

const app = express();
const port = 3000;

app.use(cors());
app.use(express.json()); // Middleware para parsear JSON

app.get("/", (req, res) => {
    res.send("hola hojjla");
});

app.post("/create_preference", async (req, res) => {
    try {
        console.log("Request body:", req.body); // Log el cuerpo de la solicitud

        if (!req.body || !req.body.title) {
            throw new Error("Request body or title is missing");
        }

        const body = {
            items: [
                {
                    title: req.body.title,
                    quantity: Number(req.body.quantity),
                    unit_price: Number(req.body.price),
                    currency_id: "CLP",
                },
            ],
            back_urls: {
                success: "https://www.youtube.com",
                failure: "https://www.youtube.com",
                pending: "https://www.youtube.com",
            },
            auto_return: "approved",
        };

        console.log("Preference to be created:", body); // Log la preferencia a ser creada

        const preference = new Preference(client);
        const result = await preference.create({ body });
        console.log("Preference creation response:", result); // Log la respuesta de Mercado Pago

        res.json({
            id: result.id,
        });

    } catch (error) {
        console.error("Error creating preference:", error);
        res.status(500).json({
            error: "error noma",
            details: error.message || error,
        });
    }
});

app.listen(port, () => {
    console.log(`el servidor está corriendo en el puerto ${port}`);
});
