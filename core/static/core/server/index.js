
import express from "express";
import cors from "cors";
import { MercadoPagoConfig, Preference } from 'mercadopago';



const client = new MercadoPagoConfig({ accessToken: 'TEST-7400591541742198-050923-6fedd8b527f928b3112f0b3b4ae84957-1451079063' });


const app = express()
const port = 3000;

app.use(cors());
app.use(express());

app.get("/", (req, res) => {
    res.send("hola hojjla")
});

app.post("/create_preference", async (req, res) => {
    try {
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
        const preference = new Preference(client);
        const result = await preference.create({ body });
        res.json({
            id: result.id,
        });

    } catch (error){
        console.log(error)
        res.status(500).json({
            error: "error noma"
        });

    }
});


app.listen(port, () => {
    console.log(`el servidos esta corriendo en el puerto ${port}`)
});
