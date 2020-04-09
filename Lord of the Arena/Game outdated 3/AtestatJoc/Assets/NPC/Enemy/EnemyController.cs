using UnityEngine;
using System.Collections;

public class EnemyController : MonoBehaviour {
	public int Health = 150;
	public GameObject onFire;
	public GameObject Frozen;
	public bool isFrozen = false;
	public bool isOnFire = false;
	public bool isFrozenNow = false;
	public bool isOnFireNow = false;
	public bool isIncinerated = false;
	public bool isIncineratedNow = false;
	private float debuffDuration;
// Update
	
	void Start(){
		
	}
	void Update () {
		if(isFrozen){
		//TO DO : when movement speed and pathfinding is added slow move speed
		//REMEMBER debuffs will last 5 seconds : will freeze for 5 seconds/will damage for 5 seconds
			GameObject debuffFrozen = (GameObject)Instantiate(Frozen,transform.position,Quaternion.identity);
			debuffFrozen.transform.parent = transform;
			isFrozen = false;
			isFrozenNow = true;
		}
		if(isOnFire){ 
			GameObject debuffOnFire = (GameObject)Instantiate(onFire,transform.position,Quaternion.identity);
			debuffOnFire.transform.parent = transform;
			isOnFireNow=true;
			isOnFire=false;
				}
		if (isIncinerated) {
			GameObject debuffIncinerated = (GameObject)Instantiate(onFire,transform.position,Quaternion.identity);
			debuffIncinerated.transform.parent = transform;
			debuffIncinerated.GetComponent<OnFire>().damage=20;
			isIncineratedNow=true;
			isIncinerated=false;
		}
		}
	
	
	public void TakeDamage(int Damage){
	Health-=Damage;
	if(Health<=0)Destroy (gameObject);
	}
	
	public int GetHealth(){
		return Health;
	}
	
}
