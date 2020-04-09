using UnityEngine;
using System.Collections;

public class FireBall_Explosion : MonoBehaviour {
	public int damage = 100;
	
	void Start(){
	Destroy(gameObject,0.25f);	
	}
	
	void OnTriggerEnter2D(Collider2D col){
		if(col.tag == "Enemy"){
			col.GetComponent<EnemyController>().TakeDamage(damage);
	}
	}
}
