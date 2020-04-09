using UnityEngine;
using System.Collections;

public class Default : MonoBehaviour {
	public int damage = 25;
	
	public void HitTarget(){
		Destroy (gameObject);
	}
	
	void OnTriggerEnter2D(Collider2D col){
		if(col.tag == "Enemy"){
			col.GetComponent<EnemyController>().TakeDamage(damage);//EnemyController Enemy = 
	}
		Destroy(gameObject);
	}
}
