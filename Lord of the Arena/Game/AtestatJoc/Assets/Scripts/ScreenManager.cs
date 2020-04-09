using UnityEngine;
using System.Collections;

public class ScreenManager : MonoBehaviour {
	public GameObject PauseScreen;
	public GameObject InventoryScreen;
	// Use this for initialization
	void Start () {
	
	}
	
	// Update is called once per frame
	void Update () {
		if (Input.GetKeyDown (KeyCode.Escape)) {
			Time.timeScale = 0;
			PauseScreen.gameObject.SetActive(true);
		}
		if (Input.GetKeyDown (KeyCode.I)) {
			Time.timeScale = 0;
			InventoryScreen.gameObject.SetActive(true);
		}

	}
}
