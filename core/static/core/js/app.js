document.addEventListener("DOMContentLoaded", function () {
    const mp = new MercadoPago('TEST-99b079b4-d97b-4ea4-bf60-23112846af0a', {
        locale: "es-AR",
    });

    document.getElementById("checkoutBtn").addEventListener("click", async () => {
        try {
            const orderData = {
                title: "producto",
                quantity: 1,
                price: 1,
            };

            console.log("Sending order data:", orderData); // Log los datos que se envían

            const response = await fetch("http://localhost:3000/create_preference", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(orderData),
            });

            if (!response.ok) {
                const errorDetails = await response.json();
                console.error("Error in response:", errorDetails);
                throw new Error(errorDetails.error);
            }

            const preference = await response.json();
            console.log("Received preference:", preference);

            createCheckoutButton(preference.id);

        } catch (error) {
            console.error("Error creating preference:", error);
            alert("error :c");
        }
    });

    const createCheckoutButton = (preferenceId) => {
        const bricksBuilder = mp.bricks();

        const renderComponent = async () => {
            if (window.checkoutButton) window.checkoutButton.unmount();

            try {
                await bricksBuilder.create("wallet", "wallet_container", {
                    initialization: {
                        preferenceId: preferenceId,
                    },
                    customization: {
                        texts: {
                            valueProp: 'smart_option',
                        },
                    },
                });
            } catch (error) {
                console.error("Error rendering component:", error);
            }
        };
        renderComponent();
    };
});
