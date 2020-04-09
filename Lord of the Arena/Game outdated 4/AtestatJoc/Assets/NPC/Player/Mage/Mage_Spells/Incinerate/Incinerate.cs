using UnityEngine;
using System.Collections;

public class Incinerate : MonoBehaviour {
	public int defaultDamage= 20;
	public int damage = 20;
	
	void Start(){
		Destroy (gameObject, 0.5f);
	}
	
	void OnTriggerEnter2D(Collider2D col){
		if(col.tag == "Enemy"){
			EnemyController enemy = col.GetComponent<EnemyController>();
			if(!enemy.isIncineratedNow && !enemy.isOnFireNow)enemy.isIncinerated = true;
	}
	}
}
