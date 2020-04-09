using UnityEngine;
using System.Collections;

public class PauseScreen : MonoBehaviour {
	
	// Update is called once per frame
	void Update () {
		if (Input.GetKeyDown (KeyCode.Escape)) {
			Time.timeScale = 1;
			gameObject.SetActive(false);
		}
	}

	public void UnPause(){
		Time.timeScale = 1;
		gameObject.SetActive (false);
	}
}
