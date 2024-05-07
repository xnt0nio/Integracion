const mp = new MercadoPago('YOUR_PUBLIC_KEY', {
    locale: "es-CH",
});

document.getElementById("checkout-btn").addEventListener("click",async () =>{
    try{


        const orderData = {
            title: "producto",
            quanty: 1,
            price: 10,
        };
    
        const response  = await  fetch("http://localhost:3000/create_preference", {
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