// $(document).ready(function() {

//   $.get('https://fakestoreapi.com/products',

//     function(registros){

//       var ropaHTML = $('#premio').prop('outerHTML');
//       ropaHTML = ropaHTML.replace('d-none', '');

//       $('#lista').empty();

//       $.each(registros, function(i, item) {

//         // Crear el codigo HTML para agegar un recuadro a la lista de premios
//         recuadro = ropaHTML;
//         recuadro = recuadro.replace('src=""', `src="${item.image}"`);
//         recuadro = recuadro.replace('[[nombre]]', item.title);
//         recuadro = recuadro.replace('[[precio]]', item.price);
//         recuadro = recuadro.replace('[[descripcion]]', item.description);
        
//         // Agregar el recuadro a la lista de premios
//         $('#lista').append(recuadro);
      
//     });

//     setTimeout(`
//       $('#imagen-de-espera').hide();
//       $('#capa-cubre-todo').hide();
//       `, 2000);

//   });

// });


fetch("http://fakestoreapi.com/products")
.then((response) => response.json())
.then((data) => {
  const container = document.getElementById("container");
  data.forEach((product) => {
    const productCard = document.createElement("div");
    productCard.classList.add("col", "p-2", "d-flex");
    const truncatedDescription =
      product.description.substring(0, 200) +
      (product.description.length > 200 ? "..." : "");

      productCard.innerHTML = `
      <div class="col">
        <div class="card mb-4 box-shadow">
          <div class="card pt-2 flex-column text-center" style="height: 500px">
            <img src="${product.image}" style="height: 350px; max-width: 100%; object-fit: contain;" class="caratulas"/>
          </div>
          <div class="card-body">
            <h5 class="card-title">${product.title}</h5>
              <div class="card-text">
                <div class="lead text-terciary">${truncatedDescription}</div>
                <br/>
              </div>
              <div class="card-footer">
                <div class="lead">
                  <span class="sale-real-price fw-bold">$${product.price}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    `;
    container.appendChild(productCard);
  });
});

{/* <div class="col">
<div class="card pt-2 flex-column" style="height: 500px">
  <img src="${product.image}" class="card-img-top" alt="${product.title}" />
  <div class="card-body">
    <h5 class="card-title">${product.title}</h5>
    <p class="card-text card-footer titledesc">
      <span class="index_precio">$${product.price}</span>
      <br>
      <span class="lower-text">${truncatedDescription}</span>
    </p>
  </div>
</div>
</div> */}