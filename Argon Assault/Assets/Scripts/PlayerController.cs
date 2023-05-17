using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.InputSystem;

public class PlayerController : MonoBehaviour
{
    [Header("General Setup Settings")]
    [SerializeField] InputAction movement;
    [SerializeField] InputAction firing;
    [Tooltip("How fast ship moves up, down, left, right based on player input")] [SerializeField] float speedMultiplier = 10f;
    [Tooltip("How far the player can move on the x axis. From -xRange to +xRange.")] [SerializeField] float xRange = 5f;
    [Tooltip("How far the player can move on the y axis. From -yRange to +yRange.")] [SerializeField] float yRange = 5f;

    [Header("Lasers gun array")]
    [SerializeField] GameObject[] lasers;

    [Header("Screen Position based tuning")]
    [SerializeField] float pitchPositionFactor = -2f;
    [SerializeField] float yawPositionFactor = -1.5f;

    [Header("Player input based tuning")]
    [SerializeField] float pitchControlFactor = -10f;
    [SerializeField] float rollControlFactor = -10f;
    
    [Header("Input System Smoothing")]
    [SerializeField] float smoothInputSpeed = .1f;

    float yThrow;
    float xThrow;

    Vector2 currentInputVector;
    Vector2 smoothInputVelocity;

    void OnEnable() {
        movement.Enable();
        firing.Enable();
    }

    void OnDisable() {
        movement.Disable();
        firing.Disable();
        SetLasersActive(false);
    }

    // Update is called once per frame
    void Update()
    {
        ProcessInput();
        ProcessTranslation();
        ProcessRotation();
        ProcessFiring();
    }

    void ProcessInput(){
        float currentInputX = movement.ReadValue<Vector2>().x;
        float currentInputY = movement.ReadValue<Vector2>().y;

        
        currentInputVector = Vector2.SmoothDamp(currentInputVector, new Vector2(currentInputX, currentInputY), ref smoothInputVelocity, smoothInputSpeed);

        xThrow = currentInputVector.x;
        yThrow = currentInputVector.y;
    }

    void ProcessTranslation()
    {
        float rawPosX = transform.localPosition.x + xThrow * Time.deltaTime * speedMultiplier;
        float clampedPosX = Mathf.Clamp(rawPosX, -xRange, xRange);

        float rawPosY = transform.localPosition.y + yThrow * Time.deltaTime * speedMultiplier;
        float clampedPosY = Mathf.Clamp(rawPosY, -yRange, yRange);

        transform.localPosition = new Vector3(
            clampedPosX,
            clampedPosY,
            transform.localPosition.z
        );
    }

    void ProcessRotation(){
        float pitchDueToPosition = transform.localPosition.y * pitchPositionFactor;
        float pitchDueToControl = yThrow * pitchControlFactor;

        float yawDueToPosition = transform.localPosition.x * yawPositionFactor;

        float rollDueToControl = xThrow * rollControlFactor;

        float pitch = pitchDueToPosition + pitchDueToControl;
        float yaw = yawDueToPosition;
        float roll = rollDueToControl;

        transform.localRotation = Quaternion.Euler(pitch, yaw, roll);
    }

    void ProcessFiring(){
        if(firing.ReadValue<float>() == 1){
            SetLasersActive(true);
        } else {
            SetLasersActive(false);
        }
    }

    void SetLasersActive(bool active){
        foreach(GameObject laser in lasers){
            var emissionModule = laser.GetComponent<ParticleSystem>().emission;
            emissionModule.enabled = active;
        }
    }
}
