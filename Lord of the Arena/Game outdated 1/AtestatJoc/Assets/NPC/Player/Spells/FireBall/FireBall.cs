using UnityEngine;
using System.Collections;

public class FireBall : MonoBehaviour {
	public int damage = 75;
	public GameObject FireBall_Explosion;
	public void HitTarget(){
		Destroy (gameObject);
	}
	
	void OnTriggerEnter2D(Collider2D col){
		if(col.tag == "Enemy"){
			col.GetComponent<EnemyController>().TakeDamage(damage);//EnemyController Enemy = 
	}
		Instantiate (FireBall_Explosion,transform.position,Quaternion.identity);
		Destroy(gameObject);
	}
}
