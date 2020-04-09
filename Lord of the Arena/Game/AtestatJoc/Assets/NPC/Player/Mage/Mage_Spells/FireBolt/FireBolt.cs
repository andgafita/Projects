using UnityEngine;
using System.Collections;

public class FireBolt : MonoBehaviour {
	public int defaultDamage = 25;
	public int damage = 25;
	
	public void HitTarget(){
		Destroy (gameObject);
	}
	
	void OnTriggerEnter2D(Collider2D col){
		if(col.tag == "Enemy"){EnemyController enemy = col.GetComponent<EnemyController>();
			if(!enemy.isOnFireNow && !enemy.isIncineratedNow)enemy.isOnFire = true;
			enemy.TakeDamage(damage);
	}
		Destroy(gameObject);
	}
}
