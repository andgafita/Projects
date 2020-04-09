using UnityEngine;
using System.Collections;

public class OnFire : MonoBehaviour {
	public int damage = 10;
	
	private float duration;
	private int ticks = 5;
	void Start(){
	duration = Time.realtimeSinceStartup;
	Debug.Log("fire spawned");
	}
	
	
	void OnTriggerStay2D (Collider2D col) {
		//Debug.Log(duration);
		if(col.tag == "Enemy"){
			//try to occur every 1 second more or less
			if(duration+1 <= Time.realtimeSinceStartup){
			duration++;ticks--;
			col.GetComponent<EnemyController>().TakeDamage(damage);
			//check if the debuff is over
			if(ticks==0){
			col.GetComponent<EnemyController>().isOnFireNow=false;
			Destroy(gameObject);
						}
					}
				}
	}
	
	
	
	
}
