using UnityEngine;
using System.Collections;

public class InventoryScreen : MonoBehaviour {
	public GameObject Something;
	public struct Item{
		public string name;
		public int Intellect, Strength, Endurance, Stamina;
		public int gold;
	}
	
	// Update is called once per frame
	void Update () {
		if (Input.GetKeyDown (KeyCode.I)) {
			Time.timeScale = 1;
			gameObject.SetActive(false);
		}
	}
	public void makeAppear(){
		Instantiate(Something,Camera.main.ScreenToWorldPoint(transform.position),Quaternion.identity);
	}
}
