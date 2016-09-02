from firebase import firebase
firebase = firebase.FirebaseApplication('https://electeng209-520f4.firebaseio.com/', authentication=None)
firebase.delete('/data', None)
