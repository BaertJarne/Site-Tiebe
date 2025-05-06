'use strict';
const lanIP = `${window.location.hostname}:8000`;
const socketio = io(lanIP);

// #region ***  DOM references                           ***********
let htmlFormAdd;
let fotos, teksten, combined;
// #endregion

// #region ***  Callback-Visualisation - show___         ***********
const showFotosTeksten = () => {
  console.log('enterd show');

  // console.log('Voor replace enters in teksten');
  // console.log(json);
  for (let i = 0; i < teksten.length; i++) {
    teksten[i].tekstje = teksten[i].tekstje.replace(/\n/g, '<br>');
    // console.log(teksten[i]);
  }
  // console.log('Na replace enters in teksten');
  // console.log(teksten);

  let output = '';
  let used = [];
  combineFotosWithTekst();

  while (used.length != combined.length) {
    // console.log(Math.floor(Math.random() * combined.length))
    let random_place = Math.floor(Math.random() * combined.length);
    while (used.includes(random_place) == true) {
      random_place = Math.floor(Math.random() * combined.length);
      // console.log(Math.floor(Math.random() * combined.length))
    }
    // console.log(random_place);
    used.push(random_place);
    // console.log('used list:');
    // console.log(used);

    const list_tekst_foto = combined[random_place];
    console.log(list_tekst_foto);

    if (list_tekst_foto[2] == 0) {
      output += `<article class="o-main__article c-grid">
                  <img class="c-img c-right__grid c-grid__content" src="img/met_db/${list_tekst_foto[1]}" alt="Foto Tiebe Blanckaert">
                  <p class="c-tekst c-left__grid c-grid__content">${list_tekst_foto[0]}</p>
                </article>`;
    } else if (list_tekst_foto[2] == 1) {
      output += `<article class="o-main__article c-grid">
                  <p class="c-tekst c-right__grid c-grid__content">${list_tekst_foto[0]}</p>
                  <img class="c-img c-left__grid c-grid__content" src="img/met_db/${list_tekst_foto[1]}" alt="Foto Tiebe Blanckaert">
                </article>`;
    } else if (list_tekst_foto[2] == 2) {
      output += `<article class="o-main__article c-grid_1">
                  <img class="c-img_1 c-grid__content" src="img/met_db/${list_tekst_foto[1]}" alt="Foto Tiebe Blanckaert">
                </article>`;
    } else if (list_tekst_foto[2] == 3) {
      output += `<article class="o-main__article c-grid_1">
                  <p class="c-tekst_1 c-grid__content">${list_tekst_foto[0]}</p>
                </article>`;
    } else {
      console.log('foute mogelijkheid');
    }
  }

  // console.log(output);
  document.querySelector('.js-fotos-tekst').innerHTML = output;
};
// #endregion

// #region ***  Callback-No Visualisation - callback___  ***********
const callbackAdd = () => {
  console.log("Foto's en/of tekst is sucsesvol toegevoegd");
  window.location.href = 'index.html';
};
// #endregion

// #region ***  Data Access - get___                     ***********
const GetFotos = async () => {
  const url = `http://${lanIP}/api/v1/foto/`;
  const response = await fetch(url).catch((err) => console.error('Fetch-error:', err));
  console.log(response);
  const json = await response.json().catch((err) => console.error('JSON-error:', err));
  console.log(json);
  fotos = json;
  GetTeksten();
};

const GetTeksten = async () => {
  const url = `http://${lanIP}/api/v1/tekst/`;
  const response = await fetch(url).catch((err) => console.error('Fetch-error:', err));
  const json = await response.json().catch((err) => console.error('JSON-error:', err));
  teksten = json;
  // console.log(teksten);
  showFotosTeksten();
};

const getPostFotoToFolder = async (foto) => {
  const formData = new FormData();
  formData.append('file', foto);
  // const body = JSON.stringify({
  // paden: foto,
  // });

  const url = `http://${lanIP}/api/v1/fotoToFolder/`;
  const response = await fetch(url, {
    method: 'POST',
    // headers: { 'Content-Type': 'application/json' },
    body: formData,
  }).catch((err) => console.error('Fetch-error:', err));
  const json = await response.json().catch((err) => console.error('JSON-error:', err));
  // console.log(json.name);
  return json.name;
};

const GetPostFotoToDB = async (naam) => {
  const body = JSON.stringify({
    paden: naam,
  });

  const url = `http://${lanIP}/api/v1/fotoToDB/`;
  console.log(body, url);
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: body,
  }).catch((err) => console.error('Fetch-error:', err));
  // console.log(response);
  const json = await response.json().catch((err) => console.error('JSON-error:', err));
  // console.log(json);
  return json;
};

const GetPostTekst = async (tekst, idfoto) => {
  const body = JSON.stringify({
    tekstje: tekst,
    idfoto: idfoto,
  });

  const url = `http://${lanIP}/api/v1/tekstje/`;
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: body,
  }).catch((err) => console.error('Fetch-error:', err));
  const json = await response.json().catch((err) => console.error('JSON-error:', err));
  // console.log(json);
};

const addFotoTekst = async () => {
  const tekst = document.querySelector('.js-form__textarea').value;
  const img = document.querySelector('.js-form__file');
  console.log(img);

  if ((tekst || img.value) != '') {
    if (img.value != '') {
      let allPaths
      for (const file of img.files) {
        // let filenaam = '';
        const filenaam = await getPostFotoToFolder(file);
        // console.log(filenaam);
        allPaths = await GetPostFotoToDB(filenaam);
        // console.log(tekst)
        // console.log(allPaths)
      }
      if (tekst != '') {
        let nieuwID = 0;
        for (let path of allPaths) {
          nieuwID = path.idfoto_paden;
        }

        // console.log(nieuwID)
        GetPostTekst(tekst, nieuwID);
      }
    } else {
      GetPostTekst(tekst, 0);
    }
    callbackAdd();
  }
  listenToAdd();
};

const combineFotosWithTekst = () => {
  let tekstenCopy = teksten;
  let fotosCopy = fotos;
  let fotosToDel = [];
  combined = []; //3de element: 2 == enkel foto links, 2 == enkel foto recht, 4 == enkel tekst rechts, 5 == enkel tekst links , 0 == foto links tekst rechts, 1 == foto rechts tekst links
  for (const tekst of tekstenCopy) {
    const random_number = Math.floor(Math.random() * 2);
    if (tekst.idfoto != 0) {
      combined.push([tekst.tekstje, fotosCopy[tekst.idfoto - 1].paden, random_number]);
      fotosToDel.push(fotosCopy[tekst.idfoto - 1]);
    } else {
      combined.push([tekst.tekstje, '', 3]);
    }
  }
  // console.log(`fotosToDel:`);
  // console.log(fotosToDel);
  for (let i = 0; fotosToDel.length > i; i++) {
    fotosCopy.splice(fotosToDel[i].idfoto_paden - fotosToDel.length, 1);
    // console.log(`fotosCopy:`);
    // console.log(fotosCopy);
  }
  for (const foto of fotosCopy) {
    combined.push(['', foto.paden, 2]);
  }
  // console.log(combined);
};
// #endregion

// #region ***  Event Listeners - listenTo___            ***********
const listenToAdd = () => {
  htmlFormAdd.addEventListener('click', addFotoTekst);
};

const listenToSocket = () => {
  socketio.on('B2F_connected', (json) => {
    console.log(`Eerste boodschap server:`);
    console.log(json.status);
    teksten = json.teksten;
    fotos = json.fotos;
    showFotosTeksten();
  });

  socketio.on('connect', () => {
    console.log(`verbonden met socketio-server`);
  });

  socketio.on('B2F_new_content_added', (json) => {
    console.log(json.status);
    teksten = json.teksten;
    fotos = json.fotos;
    showFotosTeksten();
  });
};
// #endregion

// #region ***  Init / DOMContentLoaded                  ***********
const init = () => {
  console.info('init geladen');
  const htmlPagIndex = document.querySelector('.js-pagina-index');
  const htmlPagAdd = document.querySelector('.js-pagina-aanpassen');
  listenToSocket();

  if (htmlPagIndex) {
    console.log('index pagina');
  }

  if (htmlPagAdd) {
    console.log('Add pagina');
    htmlFormAdd = document.querySelector('.js-form__button-add');
    listenToAdd();
  }
};

document.addEventListener('DOMContentLoaded', init);
// #endregion
