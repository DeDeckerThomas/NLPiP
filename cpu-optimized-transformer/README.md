# CPU optimized transformer

This directory contains everything you need to deploy the cpu optimized transformer scenario.

## 💾 Installation


### Build custom NVIDIA Triton backend image
First you need to build the custom triton-backend docker image. Check the README of the triton-backend-files directory for more information.

### Create Kubernetes Cluster
Once this is done, you can start creating the Google Kubernetes Engine. If you already have a Kubernetes cluster, then you can skip to the creation of the CPU-pool.

First create a network, if you already have an network then you can skip this.

```bash
gcloud compute networks create transformers-network --subnet-mode=custom --bgp-routing-mode=regional
```

Now create your [private standard Kubernetes Cluster](https://cloud.google.com/kubernetes-engine/docs/how-to/private-clusters). Please fill in the missing parameters with your parameters. If you want to change some parameters, please feel free to go to the documentation: 
https://cloud.google.com/sdk/gcloud/reference/container/clusters/create.


```bash
gcloud container clusters create "fast-transformers-cluster" \
--zone "your preferred zone" \
--no-enable-basic-auth \
--num-nodes "2" \
--enable-private-nodes \
--master-ipv4-cidr 10.0.0.0/28 \
--enable-ip-alias \
--network "your preferred network" \
--create-subnetwork name=cluster-subnet  \
--no-enable-intra-node-visibility \
--no-enable-master-authorized-networks \ 
--node-locations "your preferred location" \
```

### Create the CPU pool

Once the Kubernetes cluster is created, you can create the CPU pool.

```bash
gcloud container node-pools create "cpu-pool" \
--cluster "your cluster name" \
--zone "your preferred zone" \
--machine-type "n2-standard-4" \
--min-cpu-platform "Intel Ice Lake" \ 
--node-locations "your preferred location"" \
```

### Next steps
Now everything is ready for deployment with kubectl. Execute the following command to get access to the cluster with kubectl.

```bash
gcloud container clusters get-credentials your-cluster --zone="the zone of your cluster"
```

Okay now you can go to the deploy directory to finish the deployment.


## ✨ Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
