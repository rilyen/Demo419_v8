using UnityEngine;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

// Sources used to create this script:
//  - https://www.youtube.com/watch?v=-FhvQDqmgmU&list=PLwyUzJb_FNeTQwyGujWRLqnfKpV-cj-eO&ab_channel=iHeartGameDev
//  - https://github.com/ConorZAM/Python-Unity-Socket

public class animationStateController : MonoBehaviour
{
    Animator animator;
    int isFearfulHash;
    int isPumpupHash;
    int isRelaxingHash;
    int isSadHash;


    // Socket stuff
    Thread thread;
    public int connectionPort = 25001;
    TcpListener server;
    TcpClient client;
    bool running;

    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        animator = GetComponent<Animator>();
        isFearfulHash = Animator.StringToHash("isFearful");
        isPumpupHash = Animator.StringToHash("isPumpup");
        isRelaxingHash = Animator.StringToHash("isRelaxing");
        isSadHash = Animator.StringToHash("isSad");

        // Receive on a separate thread so Unity doesn't freeze waiting for data
        ThreadStart ts = new ThreadStart(GetData);
        thread = new Thread(ts);
        thread.Start();
    }

    void GetData()
    {
        // Create the server
        server = new TcpListener(IPAddress.Any, connectionPort);
        server.Start();

        // Create a client to get the data stream
        client = server.AcceptTcpClient();

        // Start listening
        running = true;
        while (running)
        {
            Connection();
        }
        server.Stop();
    }

    void Connection()
    {
        // Read data from the network stream
        NetworkStream nwStream = client.GetStream();
        byte[] buffer = new byte[client.ReceiveBufferSize];
        int bytesRead = nwStream.Read(buffer, 0, client.ReceiveBufferSize);

        // Decode the bytes into a string
        string dataReceived = Encoding.UTF8.GetString(buffer, 0, bytesRead);
        
        // Make sure we're not getting an empty string
        dataReceived.Trim();
        if (dataReceived != null && dataReceived != "")
        {
            // Convert the received string of data to the format we are using
            emotion = dataReceived;
            nwStream.Write(buffer, 0, bytesRead);
        }
    }

    public string emotion = "";

    // Update is called once per frame
    void Update()
    {
        bool isFearful = animator.GetBool(isFearfulHash);
        bool isPumpup = animator.GetBool(isPumpupHash);
        bool isSad = animator.GetBool(isSadHash);
        bool isRelaxing = animator.GetBool(isRelaxingHash);

        bool fearfulPressed = string.Equals("fearful", emotion); //Input.GetKey("h");
        bool pumpupPressed = string.Equals("pumpup", emotion); //Input.GetKey("a");
        bool relaxingPressed = string.Equals("relaxing", emotion);
        bool sadPressed = string.Equals("sad", emotion); //Input.GetKey("s");

        // if player is fearful
        if (!isFearful && fearfulPressed){
            // then set isFearful boolean to be true
            animator.SetBool(isFearfulHash, true);
        }
        // if player is not fearful
        if (isFearful && !fearfulPressed){
            // then set isWalking boolean to be false
            animator.SetBool(isFearfulHash, false);
        }
        // if player is pumpup
        if (!isPumpup && pumpupPressed){
            // then set the isPumpup boolean to be true
            animator.SetBool(isPumpupHash, true);
        } 
        // if player is not pumpup
        if (isPumpup && !pumpupPressed){
            // then set isPumpup boolean to be false
            animator.SetBool(isPumpupHash, false);
        }
        // if player is sad
        if (!isSad && sadPressed){
            // then set the isPumpup boolean to be true
            animator.SetBool(isSadHash, true);
        }
        // if player is not sad
        if (isSad && !sadPressed){
            // then set isPumpup boolean to be false
            animator.SetBool(isSadHash, false);
        }
        // if player is relaxing
        if (!isRelaxing && relaxingPressed){
            // then set the isDreamy boolean to be true
            animator.SetBool(isRelaxingHash, true);
        }
        // if player is not relaxing
        if (isRelaxing && !relaxingPressed){
            // then set the isDreamy boolean to be false
            animator.SetBool(isRelaxingHash, false);
        }
    }
}
