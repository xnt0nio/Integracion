



const mp = new MercadoPago('TEST-99b079b4-d97b-4ea4-bf60-23112846af0a', {
    locale: "es-CH",
});

document.getElementById("checkout-btn").addEventListener("click",async () =>{
    try{


        const orderData = {
            title: "producto",
            quantity: 1,
            price: 10,
        };
    
        const response  = await  fetch("http://localhost:8000/create_preference", {
            method: "POST",
            headers: {
                "content-Type": "application/json",
                
            },
            body: JSON.stringify(orderData),
        });
    
        const preference = await response.JSON()
    
        createCheckoutButton(preference.id);

    } catch(error){
        alert("error")
    } 

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