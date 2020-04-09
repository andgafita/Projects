using UnityEngine;
using System.Collections;

public class IceBolt : MonoBehaviour {
	public int damage = 25;
	
	public void HitTarget(){
		Destroy (gameObject);
	}
	
	void OnTriggerEnter2D(Collider2D col){
		if(col.tag == "Enemy"){EnemyController enemy = col.GetComponent<EnemyController>();
			if(!enemy.isFrozenNow)enemy.isFrozen = true;
			enemy.TakeDamage(damage);//EnemyController Enemy = 
				
	}
		Destroy(gameObject);
	}
}
