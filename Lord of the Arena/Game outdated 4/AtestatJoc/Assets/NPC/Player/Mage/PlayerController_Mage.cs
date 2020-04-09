using UnityEngine;
using System.Collections;

public class PlayerController_Mage : MonoBehaviour {
	//Public
	public float moveSpeed = 5.0f;
	public float projectileSpeed = 10.0f;
	//Stats
	public struct stats{public int defaultHealth, defaultVitality, defaultMana;
						public int Health, Vitality, Mana;
						public int Intellect, Endurance, Stamina, Armor;
						//Intellect
						public void SetIntellect(int setIntellect){
							Intellect = setIntellect;
							Mana = defaultMana + Intellect*10;
						}
						public int GetIntellect(){return Intellect;}
						//Endurance
						public void SetEndurance(int setEndurance){
							Endurance = setEndurance;
							Vitality = defaultVitality + Endurance*10;
						}
						public int GetEndurance(){return Endurance;}
						//Stamina
						public void SetStamina(int setStamina){
							Stamina = setStamina;
							Health = defaultHealth + Stamina*15;
						}
						public int GetStamina(){return Stamina;}
						//Armor
						public void SetArmor(int setArmor){
							Armor = setArmor;
						}
						public int GetArmor(){return Armor;}
						//Set the base stats of health mana and vitality
						public void SetDefaultStats(int health, int mana, int vitality){
						defaultHealth = health;
						defaultMana = mana;
						defaultVitality = vitality;
						}
				}
	public stats Stats;
	//Spells
	public GameObject FireBolt;
	public GameObject IceBolt;
	public GameObject FireBall;
	public GameObject FireBlast;
	public GameObject Incinerate;
	public GameObject IceWave;
	public GameObject FrozenLance;
	public GameObject FrostBite;
	//Private
	private Vector2 target;
	private Vector2 direction;
	private GameObject projectile;
	//Start
	void Start(){
		Stats.SetDefaultStats(150,100,50);
		Stats.SetIntellect(3);
		Stats.SetStamina(3);
		Stats.SetEndurance(2);
		Stats.SetArmor (0);
		UpdateSpellDamage ();
		/*print (Stats.Health + "- Intellect" + Stats.Vitality + "- Stamina" + Stats.Mana);*/
	}
//Update
	void Update () {
		Movement();
		CheckForSpells();
	}

//Checks for keybindings presses for spells
	void CheckForSpells(){
		if(Input.GetKeyDown (KeyCode.Alpha1)){
			TargetMouse();
			SpawnPojectile(FireBolt,true,1f,2f);
		}
		if(Input.GetKeyDown (KeyCode.Alpha2)){
			TargetMouse();
			SpawnPojectile(IceBolt,true,1f,2f);

		}
		if(Input.GetKeyDown (KeyCode.Alpha3)){
			TargetMouse();
			SpawnPojectile(FireBall,true,1f,2f);

		}
		if(Input.GetKeyDown(KeyCode.Alpha4)){
			TargetMouse();
			SpawnPojectile(FireBlast,false,1.5f,1f);

										}
										
		if (Input.GetKeyDown (KeyCode.Alpha5)) {
			projectile = (GameObject)Instantiate(Incinerate,transform.position,Quaternion.identity);

											}
											
		if (Input.GetKeyDown (KeyCode.Alpha6)) {
			projectile = (GameObject)Instantiate(IceWave,transform.position,Quaternion.identity);

											}
		
		if (Input.GetKeyDown (KeyCode.Alpha7)) {
			TargetMouse();
			SpawnPojectile(FrozenLance,true,1f,2f);

											}
		if (Input.GetKeyDown (KeyCode.Alpha8)) {
			projectile = (GameObject)Instantiate(FrostBite,Camera.main.ScreenToWorldPoint(Input.mousePosition),Quaternion.identity);


		}
	}

	//Updates The Spell Damage
	void UpdateSpellDamage(){
		int SpellPower = Stats.GetIntellect () * 10;
		FireBolt.GetComponent<FireBolt>().damage = FireBolt.GetComponent<FireBolt>().defaultDamage + SpellPower;
		IceBolt.GetComponent<IceBolt>().damage = IceBolt.GetComponent<IceBolt>().defaultDamage + SpellPower;
		FireBall.GetComponent<FireBall>().damage = FireBall.GetComponent<FireBall>().defaultDamage + SpellPower;
		FireBlast.GetComponent<FireBlast>().damage = FireBlast.GetComponent<FireBlast>().defaultDamage + SpellPower;
		Incinerate.GetComponent<Incinerate>().damage = Incinerate.GetComponent<Incinerate>().defaultDamage + SpellPower;
		IceWave.GetComponent<IceWave>().damage = IceWave.GetComponent<IceWave>().defaultDamage + SpellPower;
		FrozenLance.GetComponent<FrozenLance>().damage = FrozenLance.GetComponent<FrozenLance>().defaultDamage + SpellPower;
		FrostBite.GetComponent<FrostBite>().damage = FrostBite.GetComponent<FrostBite>().defaultDamage + SpellPower;
	}
//Targets Mouse
	void TargetMouse(){
		target = Camera.main.ScreenToWorldPoint(Input.mousePosition);
		direction = target - ((Vector2)transform.position);	
		direction.Normalize();
	}
	
//Cast given spell																			
	void SpawnPojectile(GameObject spawnThis, bool hasVelocity,float distanceMultiplier,float distanceDivider){
		projectile = Instantiate(spawnThis, (Vector2)transform.position+((direction*distanceMultiplier)/distanceDivider),Quaternion.identity) as GameObject;
		if(hasVelocity)projectile.rigidbody2D.velocity += direction*projectileSpeed;
			else projectile.transform.position = (Vector2)projectile.transform.position + ((direction*distanceMultiplier)/distanceDivider);
		RotateProjectile(projectile);
	}
	
//Rotates Projectile so it looks good
	void RotateProjectile(GameObject projectile){
		/*float angle = Mathf.Atan2(projectile.rigidbody2D.velocity.y,projectile.rigidbody2D.velocity.x) * Mathf.Rad2Deg;*/
		float angle = Mathf.Atan2(direction.y,direction.x) * Mathf.Rad2Deg;
		projectile.transform.rotation = Quaternion.AngleAxis(angle,Vector3.forward);
	}
	
//Player Movement
	private void Movement(){
		
		if(Input.GetKey(KeyCode.W)){
			transform.position += new Vector3(0.0f,moveSpeed*Time.deltaTime,0.0f);
		}
		if(Input.GetKey(KeyCode.S)){
			transform.position += new Vector3(0.0f,-moveSpeed*Time.deltaTime,0.0f);
		}
		if(Input.GetKey(KeyCode.D)){
			transform.position += new Vector3(moveSpeed*Time.deltaTime,0.0f,0.0f);
		}
		if(Input.GetKey(KeyCode.A)){
			transform.position += new Vector3(-moveSpeed*Time.deltaTime,0.0f,0.0f);
		}
	}
	
}
