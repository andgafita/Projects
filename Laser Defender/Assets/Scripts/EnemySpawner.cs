using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EnemySpawner : MonoBehaviour
{
    [SerializeField] List<WaveConfigSO> waveConfigs;
    [SerializeField] float timeBetweenWaves = 0f;
    [SerializeField] bool isLooping = true;
    WaveConfigSO currentWave;

    void Start()
    {
        StartCoroutine(SpawnEnemyWaves());
    }

    void setCurrentWave(WaveConfigSO wave){
        currentWave = wave;
    }

    public WaveConfigSO GetCurrentWave(){
        return currentWave;
    }

    IEnumerator SpawnEnemyWaves(){
        do {
            foreach(WaveConfigSO wave in waveConfigs){
                setCurrentWave(wave);

                for(int enemyNo = 0; enemyNo < currentWave.getEnemyCount(); enemyNo++){
                    Instantiate(currentWave.getEnemyPrefab(enemyNo), 
                                currentWave.GetStartingWaypoint().position,
                                Quaternion.Euler(0, 0, 180),
                                transform
                                );

                    yield return new WaitForSeconds(currentWave.GetRandomSpawnTime());
                }

                yield return new WaitForSeconds(timeBetweenWaves);
            }
        } while(isLooping);
    }
}
