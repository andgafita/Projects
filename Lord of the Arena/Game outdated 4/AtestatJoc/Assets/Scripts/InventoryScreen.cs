using UnityEngine;
using System.Collections;

public class InventoryScreen : MonoBehaviour {
	
	// Update is called once per frame
	void Update () {
		if (Input.GetKeyDown (KeyCode.I)) {
			Time.timeScale = 1;
			gameObject.SetActive(false);
		}
	}

}
