



document.addEventListener("DOMContentLoaded", function () {
    const mp = new MercadoPago('TEST-99b079b4-d97b-4ea4-bf60-23112846af0a', {
        locale: "es-CH",
    });

    document.getElementById("checkoutBtn").addEventListener("click", async () => {
        try {
            const orderData = {
                title: "producto",
                quantity: 1,
                price: 10,
            };

            const response = await fetch("http://localhost:3000/create_preference", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(orderData),
            });

            const preference = await response.json();
            console.log(preference);
            createCheckoutButton(preference.id);

        } catch (error) {
            alert("error :c");
        }
    });


    
    const createCheckoutButton = (preferenceId) => {
        const bricksBuilder = mp.bricks();

        const renderComponent = async () => {
            if (window.checkoutButton) window.checkoutButton.unmount();

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
        };
        renderComponent();
    };
});


const createCheckoutButton = (prederenceId) => {
    const bricksBuilder = mp.bricks();

    const renderComponent = async () =>{
        if (window.checkoutButton) window.checkoutButton.unmount();

        await bricksBuilder.create("wallet", "wallet_container", {
            initialization: {
                preferenceId: prederenceId,
            },
         customization: {
          texts: {
           valueProp: 'smart_option',
          },
          },
         });
         
    }
    renderComponent()
}