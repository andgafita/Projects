using UnityEngine;
using System.Collections;

public class Frozen : MonoBehaviour {
	//public int damage = 10;
	
	private float duration;
	private int ticks = 5;
	void Start(){
		duration = Time.realtimeSinceStartup;
	}
	
	
	void OnTriggerStay2D (Collider2D col) {
		//Debug.Log(duration);
		if(col.tag == "Enemy"){
			//check if the timer has passed
			if(duration+1 <= Time.realtimeSinceStartup){
				duration++;ticks--;
				//check if the debuff is over
				if(ticks==0){
					col.GetComponent<EnemyController>().isFrozenNow=false;
					Destroy(gameObject);
				}
			}
		}
	}
}
