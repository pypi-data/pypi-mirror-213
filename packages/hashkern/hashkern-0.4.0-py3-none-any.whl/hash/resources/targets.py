import os
import json
import yaml
from subprocess import CalledProcessError
import tempfile
import pluggy

from hash import target_hookimpl as hookimpl

from hash import errors, resources

hookspec = pluggy.HookspecMarker("hash-targets")


class TargetSpec:
    @hookspec
    def action(name: str, config: dict):
        pass

    @hookspec
    def _init(config: dict):
        pass


class Target(object):
    def _init(self, config: dict) -> None:
        self.name = config.get("name")
        if self.name is None:
            raise errors.TargetConfigError("No name specified for the target")
        self.kind = config.get("kind")
        if self.kind is None:
            raise errors.TargetConfigError("No kind specified for the target")
        self.spec = config.get("spec", {})


class FakeTarget(Target):
    @hookimpl
    def init(self, config: dict, space) -> None:
        self._init(config)
        if self.kind != "FakeTarget":
            raise errors.TargetConfigError(
                f"This target is not of kind Fake, it is of kind {self.kind}"
            )
        self.__space = space

    @hookimpl
    def action(name: str, config: dict, artifacts):
        pass


class K8STarget(Target):
    @hookimpl
    def init(self, config: dict, space) -> None:
        self._init(config)
        if self.kind != "K8STarget":
            raise errors.TargetConfigError(
                f"This target is not of kind K8S, it is of kind {self.kind}"
            )
        self.__space = space
        self.certificate_ca = None
        self.certificate = None
        self.client_key = None
        self.kube_config = None

    def remove_temp_files(self):
        if self.certificate_ca:
            try:
                os.remove(self.certificate_ca)
            except Exception:
                pass
        if self.certificate:
            try:
                os.remove(self.certificate)
            except Exception:
                pass
        if self.client_key:
            try:
                os.remove(self.client_key)
            except Exception:
                pass
        if self.kube_config:
            try:
                os.remove(self.kube_config)
            except Exception:
                pass

    def authenticate_istioctl(self) -> str:
        context = self.spec.get("context")
        kube_config = self.spec.get("kube_config")
        if context or kube_config:
            return self.authenticate_istioctl_context(context, kube_config)

    def authenticate_istioctl_context(self, context, kube_config) -> str:
        istioctl_args = ""
        if context:
            istioctl_args += f" --context=${context} "
        if kube_config:
            try:
                open(kube_config, "r")
            except FileNotFoundError:
                t = kube_config
                kube_config = tempfile.mkstemp(text=True)
                with open(kube_config[1], "w") as f:
                    f.write(t)
                self.kube_config = kube_config[1]
                istioctl_args += f" --kubeconfig {self.kube_config} "
            except OSError as e:
                if e.errno == 36:
                    t = kube_config
                    kube_config = tempfile.mkstemp(text=True)
                    with open(kube_config[1], "w") as f:
                        f.write(t)
                    self.kube_config = kube_config[1]
                    istioctl_args += f" --kubeconfig {self.kube_config} "
                else:
                    pass
        return istioctl_args

    def authenticate_kubectl(self) -> str:
        """
        Authenticate kubectl binary using the method specified in specs

        First try to use `contex` and `kube_config` files, if not defined then
        try to use direct k8s authentication using token, API server endpoint and token.
        If not defined then try using GKE specs and if not defined then try using
        AKS specs.
        """
        context = self.spec.get("context")
        kube_config = self.spec.get("kube_config")
        if context or kube_config:
            return self.authenticate_kubectl_context(context, kube_config)
        k8s = self.spec.get("k8s", {})
        if k8s and type(k8s) == dict:
            return self.authenticate_kubectl_k8s(k8s)
        gke = self.spec.get("gke", {})
        if gke and type(gke) == dict:
            return self.authenticate_kubectl_gke(gke)
        aks = self.spec.get("aks", {})
        if aks and type(aks) == dict:
            return self.authenticate_kubectl_aks(aks)

    def authenticate_kubectl_context(self, context, kube_config) -> str:
        kubectl_args = ""
        if context:
            kubectl_args += f" --context=${context} "
        if kube_config:
            try:
                open(kube_config, "r")
            except FileNotFoundError:
                t = kube_config
                kube_config = tempfile.mkstemp(text=True)
                with open(kube_config[1], "w") as f:
                    f.write(t)
                self.kube_config = kube_config[1]
            except OSError as e:
                if e.errno == 36:
                    t = kube_config
                    kube_config = tempfile.mkstemp(text=True)
                    with open(kube_config[1], "w") as f:
                        f.write(t)
                    self.kube_config = kube_config[1]
                else:
                    pass

        if self.kube_config:
            os.environ["KUBECONFIG"] = self.kube_config
        return kubectl_args

    def authenticate_kubectl_k8s(self, k8s: dict) -> str:
        kubectl_args = ""
        certificate_ca = k8s.get("certificate_ca")
        if certificate_ca:
            try:
                open(certificate_ca, "r")
            except FileNotFoundError:
                t = certificate_ca
                certificate_ca = tempfile.mkstemp(text=True)
                with open(certificate_ca[1], "w") as f:
                    f.write(t)
                self.certificate_ca = certificate_ca[1]
            except OSError as e:
                if e.errno == 36:  # File name too long
                    t = certificate_ca
                    certificate_ca = tempfile.mkstemp(text=True)
                    with open(certificate_ca[1], "w") as f:
                        f.write(t)
                    self.certificate_ca = certificate_ca[1]
                else:
                    pass  # TODO: raise error
        certificate = k8s.get("certificate")
        if certificate:
            try:
                open(certificate, "r")
            except FileNotFoundError:
                t = certificate
                certificate = tempfile.mkstemp(text=True)
                with open(certificate[1], "w") as f:
                    f.write(t)
                self.certificate = certificate[1]
            except OSError as e:
                if e.errno == 36:
                    t = certificate
                    certificate = tempfile.mkstemp(text=True)
                    with open(certificate[1], "w") as f:
                        f.write(t)
                    self.certificate = certificate[1]
                else:
                    pass
        client_key = k8s.get("client_key")
        if client_key:
            try:
                open(client_key, "r")
            except FileNotFoundError:
                t = client_key
                client_key = tempfile.mkstemp(text=True)
                with open(client_key[1], "w") as f:
                    f.write(t)
                self.client_key = client_key[1]
            except OSError as e:
                if e.errno == 36:
                    t = client_key
                    client_key = tempfile.mkstemp(text=True)
                    with open(client_key[1], "w") as f:
                        f.write(t)
                    self.client_key = client_key[1]
                else:
                    pass
        server = k8s.get("server")
        token = k8s.get("token")
        if certificate_ca and certificate and client_key:
            kubectl_args = f" --certificate-authority={certificate_ca} --client-certificate={certificate} --client-key={client_key} "
        if server:
            kubectl_args += f" --server={server} "
        if token:
            kubectl_args += f" --token={token} "
        return kubectl_args

    def authenticate_kubectl_gke(self, gke: dict) -> str:
        cluster_name = gke.get("cluster_name")
        if cluster_name is None:
            raise errors.ActionError("gke is set but gke.cluster_name is not set")
        project_id = gke.get("project_id")
        if project_id is None:
            raise errors.ActionError("gke is set but gke.project_id is not set")
        region = gke.get("region")
        if region is None:
            zone = gke.get("zone")
            if zone is None:
                raise errors.ActionError("neither region nor zone is set under gke")
            try:
                gcloud_command = f"gcloud container clusters get-credentials {cluster_name} --zone {zone} --project {project_id}"
                os.environ["KUBECONFIG"] = os.path.join(
                    self.__space.get_hash_dir(),
                    f"{cluster_name}-{zone}-{project_id}-config",
                )
                resources.Resource.execute(gcloud_command, ".")
            except CalledProcessError as e:
                raise errors.ActionError(e)
        else:
            try:
                gcloud_command = f"gcloud container clusters get-credentials {cluster_name} --region {region} --project {project_id}"
                os.environ["KUBECONFIG"] = os.path.join(
                    self.__space.get_hash_dir(),
                    f"{cluster_name}-{region}-{project_id}-config",
                )
                resources.Resource.execute(gcloud_command, ".")
            except CalledProcessError as e:
                raise errors.ActionError(e)
        return ""

    def authenticate_kubectl_aks(self, aks: dict) -> str:
        cluster_name = aks.get("cluster_name")
        if cluster_name is None:
            raise errors.ActionError("aks is set but aks.cluster_name is not set")
        subscription_id = aks.get("subscription_id")
        if subscription_id is None:
            raise errors.ActionError("aks is set but aks.subscription_id is not set")
        resource_group = aks.get("resource_group")
        if resource_group is None:
            raise errors.ActionError("aksis set but aks.resource_group is not set")
        try:
            az_command = f"az aks get-credentials --name {cluster_name} --resource-group {resource_group} --subscription {subscription_id} --overwrite-existing"
            os.environ["KUBECONFIG"] = os.path.join(
                self.__space.get_hash_dir(),
                f"{cluster_name}-{resource_group}-{subscription_id}-config",
            )
            resources.Resource.execute(az_command, ".")
        except CalledProcessError as e:
            raise errors.ActionError(e)
        return ""

    def process_kustomize(self, name: str, config: dict, kubectl_args: str):
        kubectl_binary = config.get("kubectl", "kubectl")
        manifests_path = config.get("manifests_path")
        if manifests_path is None:
            raise errors.ResourceError(f"No manifests path supplied for K8S target")
        if name == "deploy":
            kubectl_command = (
                f"{kubectl_binary} apply {kubectl_args} -f {manifests_path}"
            )
        elif name == "test" and config.get("diff") is not True:
            kubectl_command = f"{kubectl_binary} apply {kubectl_args} --dry-run=server -f {manifests_path}"
        elif name == "test" and config.get("diff") is True:
            kubectl_command = (
                f"{kubectl_binary} diff {kubectl_args} -f {manifests_path}"
            )
        try:
            resources.Resource.execute(kubectl_command, config.get("path"))
        except CalledProcessError as e:
            if config.get("diff") is True and e.returncode == 1:
                return True
            raise errors.ResourceError(e.stderr.decode("UTF-8"))
        finally:
            self.remove_temp_files()

    def process_docker_image(self, name: str, config: dict, kubectl_args: str):
        kubectl_binary = config.get("kubectl", "kubectl")
        port = config.get("port")
        if port:
            kubectl_args += f"--port={port}"
        image_url = config.get("image_url")
        if image_url is None:
            raise errors.ResourceError("No image_url supplied for K8S target")
        pod_name = config.get("pod_name")
        if pod_name is None:
            raise errors.ResourceError("No pod_name supplied for K8S target")
        kubectl_command = (
            f"{kubectl_binary} run {kubectl_args} --image={image_url} {pod_name}"
        )
        try:
            resources.Resource.execute(kubectl_command, config.get("path"))
        except CalledProcessError as e:
            raise errors.ResourceError(e.stderr.decode("UTF-8"))
        finally:
            self.remove_temp_files()

    def process_create_namespace(self, config: dict, kubectl_args: str):
        kubectl_binary = config.get("kubectl", "kubectl")
        namespace = config.get("namespace")
        if namespace is None:
            raise errors.ResourceError(
                "k8s target: create_namespace is reqested but no namespace name is provided"
            )
        kubectl_command = (
            f"{kubectl_binary} create namespace {kubectl_args} {namespace}"
        )
        try:
            resources.Resource.execute(kubectl_command, config.get("path"))
        except CalledProcessError as e:
            raise errors.ResourceError(e.stderr.decode("UTF-8"))
        finally:
            self.remove_temp_files()

    def process_delete(self, config: dict, kubectl_args: str):
        kubectl_binary = config.get("kubectl", "kubectl")
        resource_name = config.get("resource_name")
        if resource_name is None:
            raise errors.ResourceError(
                "k8s target: delete is reqested but no resource_name is provided"
            )
        resource_kind = config.get("resource_kind")
        if resource_kind is None:
            raise errors.ResourceError(
                "k8s target: delete is reqested but no resource_kind is provided"
            )
        resource_namespace = config.get("resource_namespace")
        if (
            resource_kind != "Namespace"
            and not resource_kind.startswith("Cluster")
            and not resource_namespace
        ):
            raise errors.ResourceError(
                f"k8s target: delete is reqested but no resource_namespace is provided and resource_kind is {resource_kind}"
            )
        kubectl_command = (
            f"{kubectl_binary} delete {kubectl_args} {resource_kind} {resource_name}"
        )
        if resource_namespace:
            kubectl_command += f" -n {resource_namespace}"
        try:
            resources.Resource.execute(kubectl_command, config.get("path"))
        except CalledProcessError as e:
            raise errors.ResourceError(e.stderr.decode("UTF-8"))
        finally:
            self.remove_temp_files()

    def process_istioctl_install(self, config: dict, istioctl_args: str):
        istioctl = config.get("istioctl")
        if istioctl is None or type(istioctl) != resources.IstioCtl:
            raise errors.ResourceError(
                "config['istioctl'] should be an instance of resources.IstioCtl"
            )
        istio = config.get("istio", {})
        istio_profile = istio.get("profile")
        if istio_profile:
            istioctl_args += f" --set profile={istio_profile}"
        istio_config_file = istio.get("config_file")
        if istio_config_file:
            istioctl_args += f" -f {istio_config_file} "
        revision = istio.get("revision")
        if revision:
            istioctl_args += f" -r {revision} "
        try:
            istioctl.install(istioctl_args)
        except CalledProcessError as e:
            raise errors.ResourceError(e.stderr.decode("UTF-8"))
        finally:
            self.remove_temp_files()

    def process_istioctl_verify_install(self, config: dict, istioctl_args: str):
        istioctl = config.get("istioctl")
        if istioctl is None or type(istioctl) != resources.IstioCtl:
            raise errors.ResourceError(
                "config['istioctl'] should be an instance of resources.IstioCtl"
            )
        try:
            istioctl.verify_install(istioctl_args)
        except CalledProcessError as e:
            if e.returncode == 1:
                return True
            raise errors.ResourceError(e.stderr.decode("UTF-8"))
        finally:
            self.remove_temp_files()
        return False

    def check_config(self, config: dict):
        if config.get("path") is None:
            raise errors.ResourcePublishError(
                "You need to specify path for command execution"
            )
        if config.get("kind", "Kustomize") not in ["Kustomize", "DockerImage"]:
            raise errors.ResourceDeployError(
                "Config kind must be either 'Kustomize' or 'DockerImage'"
            )

    @hookimpl
    def action(self, name: str, config: dict):
        if name not in [
            "deploy",
            "test",
            "create_namespace",
            "delete",
            "istioctl_install",
            "istioctl_verify-install",
        ]:
            raise errors.TargetActionError(
                f"Cannot run action {name} with target of type K8S"
            )
        kubectl_args = self.authenticate_kubectl()
        self.check_config(config)
        config_kind = config.get("kind", "Kustomize")
        service_account = config.get("service_account")
        if service_account:
            kubectl_args += f"--serviceaccount={service_account}"
        if name == "create_namespace":
            return self.process_create_namespace(config, kubectl_args)
        elif name == "delete":
            return self.process_delete(config, kubectl_args)
        elif name == "istioctl_install":
            istioctl_args = self.authenticate_istioctl()
            return self.process_istioctl_install(config, istioctl_args)
        elif name == "istioctl_verify-install":
            istioctl_args = self.authenticate_istioctl()
            return self.process_istioctl_verify_install(config, istioctl_args)
        if config_kind == "Kustomize":
            return self.process_kustomize(name, config, kubectl_args)
        elif config_kind == "DockerImage":
            return self.process_docker_image(name, config, kubectl_args)


class DockerRegistryTarget(Target):
    @hookimpl
    def init(self, config: dict, space) -> None:
        self._init(config)
        if self.kind != "DockerRegistryTarget":
            raise errors.TargetConfigError(
                f"This target is not of kind DockerRegistry, it is of kind {self.kind}"
            )
        self.__space = space
        self.docker_config_dir = None

    def authenticate_docker(self):
        registry_url = self.spec.get("registry_url")
        if registry_url is None:
            raise errors.ResourcePublishError("No registry_url in target")

        docker = self.spec.get("docker", {})
        if docker and type(docker) == dict:
            return self.authenticate_docker_config(docker)
        gcr = self.spec.get("gcr", {})
        if gcr and type(gcr) == dict:
            return self.authenticate_docker_gcr(gcr)
        acr = self.spec.get("acr", {})
        if acr and type(acr) == dict:
            return self.authenticate_docker_acr(acr)

    def authenticate_docker_config(self, docker: dict):
        docker_config = docker.get("config")
        if docker_config:
            self.docker_config_dir = tempfile.mkdtemp()
            with open(os.path.join(self.docker_config_dir, "config.json"), "w") as f:
                f.write(docker_config)
        else:
            credHelpers = docker.get("credHelpers")
            if credHelpers:
                self.docker_config_dir = tempfile.mkdtemp()
                with open(
                    os.path.join(self.docker_config_dir, "config.json"), "w"
                ) as f:
                    out = {"credHelpers": credHelpers}
                    json.dump(out, f)
        if self.docker_config_dir:
            os.environ["DOCKER_CONFIG"] = self.docker_config_dir

    def authenticate_docker_gcr(self, gcr: dict):
        service_account = gcr.get("service_account")
        registry_url = self.spec.get("registry_url")
        registry_host = registry_url.split("/")[0]
        login_command = f"gcloud auth print-access-token | docker login -u oauth2accesstoken --password-stdin https://{registry_host}"
        self.docker_config_dir = os.path.join(
            self.__space.get_hash_dir(),
            f"{registry_host}-local-docker-config",
        )
        if service_account:
            self.docker_config_dir = os.path.join(
                self.__space.get_hash_dir(),
                f"{registry_host}-{service_account}-docker-config",
            )
            login_command = f"gcloud auth print-access-token --impersonate-service-account {service_account} | docker login -u oauth2accesstoken --password-stdin https://{registry_host}"
        try:
            os.makedirs(self.docker_config_dir, exist_ok=True)
            os.environ["DOCKER_CONFIG"] = self.docker_config_dir
            resources.Resource.execute(login_command, ".")
        except CalledProcessError as e:
            raise errors.ResourcePublishError(e.stderr.decode("UTF-8"))

    def authenticate_docker_acr(self, acr: dict):
        registry_name = acr.get("registry_name")
        if registry_name is None:
            raise errors.ActionError("acr is set but acr.registry_name is not set")
        subscription_id = acr.get("subscription_id")
        if subscription_id is None:
            raise errors.ActionError("acr is set but acr.subscription_id is not set")
        login_command = (
            f"az acr login --subscription {subscription_id} --name {registry_name}"
        )
        self.docker_config_dir = os.path.join(
            self.__space.get_hash_dir(),
            f"{registry_name}-{subscription_id}-docker-config",
        )
        try:
            os.makedirs(self.docker_config_dir, exist_ok=True)
            os.environ["DOCKER_CONFIG"] = self.docker_config_dir
            resources.Resource.execute(login_command, ".")
        except CalledProcessError as e:
            raise errors.ResourcePublishError(e.stderr.decode("UTF-8"))

    def check_config(self, config: dict):
        if config.get("path") is None:
            raise errors.ResourcePublishError(
                "You need to specify path for command execution"
            )
        if config.get("kind", "DockerFile") not in ["DockerFile", "DockerImage"]:
            raise errors.ResourceDeployError(
                "Config kind must be either 'DockerFile' or 'DockerImage'"
            )

    def process_docker_file(self, config: dict):
        image_name = config.get("image_name")
        if image_name is None:
            raise errors.ResourcePublishError("You need to specify image name")
        registry_url = self.spec.get("registry_url")
        path = config.get("path")
        docker_file = config.get("docker_file", "Dockerfile")
        docker_file_path = config.get("docker_file_path", path)
        image_url = f"{registry_url}/{image_name}"
        build_command = (
            f"docker build -t {image_url} {docker_file_path} -f {docker_file}"
        )
        publish_command = f"docker push {image_url}"
        inspect_command = "docker inspect --format='{{.RepoDigests}}' " + image_url
        try:
            resources.Resource.execute(build_command, path)
            resources.Resource.execute(publish_command, path)
            p = resources.Resource.execute(inspect_command, path)
            image_digest = p.stdout.decode("UTF-8").replace("[", "").replace("]", "")
            image_digests = image_digest.split(" ")
            docker_image_name = image_name.split(":")[0]
            image_digest = ""
            if len(image_digests) == 1:
                if len(image_digests[0].split("@")) <= 1:
                    raise errors.ResourceError(
                        f"images digest {image_digests[0]} has no @"
                    )
                image_digest = image_digests[0].split("@")[1].strip()
            else:
                for digest in image_digests:
                    if len(digest.split("@")) <= 1:
                        raise errors.ResourceError(f"images digest {digest} has no @")
                    host_part = digest.split("@")[0]
                    if host_part == f"{registry_url}/{docker_image_name}":
                        image_digest = digest.split("@")[1].strip()
            if image_digest == "":
                raise errors.ResourceError(
                    f"Cannot find image digest for image {image_url} in {image_digests}"
                )
            image_url_digest = f"{registry_url}/{docker_image_name}@{image_digest}"
            return {"image_url": image_url, "image_url_digest": image_url_digest}
        except CalledProcessError as e:
            raise errors.ResourcePublishError(e.stderr.decode("UTF-8"))

    def process_docker_image(self, config):
        image_name = config.get("image_name")
        if image_name is None:
            raise errors.ResourcePublishError("You need to specify image name")
        registry_url = self.spec.get("registry_url")
        image_file = config.get("image_file")
        image_url = f"{registry_url}/{image_name}"
        build_command = f"docker image load -i {image_file}"
        tag_command = f"docker tag {image_name} {image_url}"
        publish_command = f"docker push {image_url}"
        path = config.get("path")
        try:
            resources.Resource.execute(build_command, path)
            resources.Resource.execute(tag_command, path)
            resources.Resource.execute(publish_command, path)
            return image_url
        except CalledProcessError as e:
            raise errors.ResourcePublishError(e.stderr.decode("UTF-8"))

    def process_inspect(self, config):
        image_name = config.get("image_name")
        if image_name is None:
            raise errors.ResourcePublishError("You need to specify image name")
        registry_url = self.spec.get("registry_url")
        image_url = f"{registry_url}/{image_name}"
        inspect_command = f"docker manifest inspect {image_url}"
        path = config.get("path")
        try:
            p = resources.Resource.execute(inspect_command, path)
            data = json.loads(p.stdout.decode("UTF-8"))
            return {"found": True, "data": data}
        except CalledProcessError as e:
            if e.returncode == 1:
                return {"found": False, "data": {}}
            raise errors.ResourceError(
                f"Error inpsecting docker image {image_url} : {e.stderr.decode('utf-8')}"
            )

    @hookimpl
    def action(self, name: str, config: dict):
        if name not in ["publish", "inspect"]:
            raise errors.TargetActionError(
                f"Cannot run action {name} with target of type Docker Registry"
            )
        self.authenticate_docker()
        self.check_config(config)
        if name == "inspect":
            return self.process_inspect(config)
        else:
            config_kind = config.get("kind", "DockerFile")
            if config_kind == "DockerFile":
                return self.process_docker_file(config)
            elif config_kind == "DockerImage":
                return self.process_docker_image(config)


class DOFunctionTarget(Target):
    def __verify_function(
        self, package_name: str, function_name: str, config: dict
    ) -> bool:
        packages = config.get("packages", [])
        for package in packages:
            if package.get("name") == package_name:
                functions = package.get("functions", [])
                for function in functions:
                    if function.get("name") == function_name:
                        return True
        return False

    @hookimpl
    def init(self, config: dict, space) -> None:
        self._init(config)
        if self.kind != "DOFunctionTarget":
            raise errors.TargetConfigError(
                f"This target is not of kind DOFunction, it is of kind {self.kind}"
            )
        self.__space = space

    @hookimpl
    def action(self, name: str, config: dict):
        if name != "deploy":
            raise errors.ResourceError(
                f"DOFunction target can only run deploy actions not {name}"
            )
        region = self.spec.get("region")
        if region is None:
            raise errors.ResourceError("No region found in DOFunction target specs")
        project_dir = config.get("project_dir")
        if project_dir is None:
            raise errors.ResourceError(
                "No project_dir provided in config for DOFunction target"
            )
        if not os.path.exists(os.path.join(project_dir, "project.yml")):
            raise errors.ResourceError(f"No project.yml file found in {project_dir}")
        package_name = config.get("package_name")
        if package_name is None:
            raise errors.ResourceError(
                "No package_name is provided for DOFunction target"
            )
        function_name = config.get("function_name")
        if function_name is None:
            raise errors.ResourceError(
                "No function_name is provided for DOFunction target"
            )
        with open(os.path.join(project_dir, "project.yml"), "r") as f:
            project_yaml = yaml.safe_load(f)
        if not self.__verify_function(package_name, function_name, project_yaml):
            raise errors.ResourceError(
                f"No package with name {package_name} and fuction with {function_name} found in {os.path.join(project_dir, 'project.yml')}"
            )
        function_index = f"{package_name}/{function_name}"
        label = self.spec.get("label")
        if label is None:
            raise errors.ResourceError("No label found in DOFunction target specs")
        namespaces_list_command = "doctl serverless namespaces list -ojson"
        namespace_id = None
        try:
            p = resources.Resource.execute(namespaces_list_command, project_dir)
            namespaces = p.stdout.decode("UTF-8")
            namespaces_list = json.loads(namespaces)
            for namespace in namespaces_list:
                if namespace.get("label") == label:
                    namespace_id = namespace.get("namespace")
        except CalledProcessError as e:
            raise errors.ResourceError(e.stdout.decode("UTF-8"))
        if namespace_id is None:
            create_namespace_command = (
                f"doctl serverless namespaces create --label {label} --region {region}"
            )
            try:
                p = resources.Resource.execute(create_namespace_command, project_dir)
                namespace_id = p.stdout.decode("UTF-8").split(" ")[4]
            except CalledProcessError as e:
                raise errors.ResourceError(
                    f"Error creating namespace in DO: {e.stderr.decode('UTF-8')}"
                )
        try:
            resources.Resource.execute(
                f"doctl serverless connect {namespace_id}", project_dir
            )
        except CalledProcessError as e:
            raise errors.ResourceError(
                f"Error connecting to namespace: {e.stderr.decode('UTF-8')}"
            )
        deploy_command = f"doctl serverless deploy . -ojson"
        try:
            resources.Resource.execute(deploy_command, config.get("project_dir"))
        except CalledProcessError as e:
            raise errors.ResourceError(e.stdout.decode("UTF-8"))
        try:
            p = resources.Resource.execute(
                f"doctl sls fn get {function_index} --url", project_dir
            )
            return p.stdout.decode("UTF-8")
        except CalledProcessError as e:
            raise errors.ResourceError(
                f"Error when getting function URL: {function_index}, {e.stderr.decode('UTF-8')}"
            )


def get_plugin_manager():
    """
    Return the plugin manager for hash-targets plugins.
    """
    pm = pluggy.PluginManager("hash-targets")
    pm.add_hookspecs(TargetSpec)
    pm.load_setuptools_entrypoints("hash-targets")
    pm.register(FakeTarget(), "FakeTarget")
    pm.register(K8STarget(), "K8STarget")
    pm.register(DockerRegistryTarget(), "DockerRegistryTarget")
    pm.register(DOFunctionTarget(), "DOFunctionTarget")
    return pm


def get_target(target, args, space):
    """
    Docs Return a target by its name

    Args:
        target (str): The name of the target to return.
        args (dict): A dictionary which contains the config for this target

    Return:
        object: The target object, which can be used to run actions
    """
    pm = get_plugin_manager()
    plugins = pm.list_name_plugin()
    for plugin in plugins:
        if target == plugin[0]:
            hash_target = plugin[1]
            hash_target.init(args, space)
            return hash_target
