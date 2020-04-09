using UnityEngine;
using System.Collections;

public class LevelManager : MonoBehaviour {

	public void ChangeLevel(string name){
		Application.LoadLevel(name);
	}
	
	public void QuitGame(){
		Application.Quit();
	}
}
