import { initializeApp } from "firebase/app";
import {getFirestore,setDoc,doc, getDoc} from "firebase/firestore"

// const firebaseConfig = {
//     apiKey: "AIzaSyAi5S3ecQ_yyC-EkGK4ID6yfDNxuAw1uyM",
//     authDomain: "moviehub-38cc2.firebaseapp.com",
//     projectId: "moviehub-38cc2",
//     storageBucket: "moviehub-38cc2.appspot.com",
//     messagingSenderId: "320027665466",
//     appId: "1:320027665466:web:d9d5cdb4cd787483448103"
//   };
  const firebaseConfig = {
    apiKey: "AIzaSyDCVhVVG2-UlMkzD8Gtw1ki325UpJipwv0",
    authDomain: "movie-hub-f7c9c.firebaseapp.com",
    projectId: "movie-hub-f7c9c",
    storageBucket: "movie-hub-f7c9c.appspot.com",
    messagingSenderId: "728786825825",
    appId: "1:728786825825:web:c2ebd48e8015bd8144b020"
  };
  const app = initializeApp(firebaseConfig);

  const db = getFirestore()


  export const updateRecommendationToFireBase = async (email,recommendationList)=>{
    const docRef = doc(db,"users",`${email}`)
    let docSnap = await getDoc(docRef)
    let fvs = docSnap.data()['Favourites']
    const payload = { Favourites : fvs , Recommended : JSON.stringify(recommendationList) }
    await setDoc(docRef,payload)
  }

  export const getUserFavouriteList = async (email)=>{
    const docRef = doc(db,"users",`${email}`)
    let docSnap = await getDoc(docRef)
    console.log(email)
    let fvstr = docSnap.data()['Favourites']
    return fvstr
  }