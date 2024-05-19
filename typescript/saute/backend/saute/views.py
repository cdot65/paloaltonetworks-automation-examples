# django imports
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.db.models.functions import Lower, Replace
from django.db.models import Value as V

# django rest framework imports
from rest_framework import viewsets, status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView


# directory object imports
from .models import (
    Panorama,
    PanoramaPlatform,
    Prisma,
    Firewall,
    FirewallPlatform,
    Jobs,
    Conversation,
    Message,
    Script,
)
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    MessageSerializer,
    PanoramaSerializer,
    PanoramaPlatformSerializer,
    PrismaSerializer,
    FirewallSerializer,
    FirewallPlatformSerializer,
    JobsSerializer,
    ScriptSerializer,
    UserSerializer,
)

# Python scripts
from .tasks import (
    execute_get_system_info as get_system_info_task,
    execute_upload_cert_chain as upload_cert_chain_task,
    execute_admin_report as admin_report_task,
    execute_assurance_arp as assurance_arp_entry_task,
    execute_assurance_readiness as assurance_readiness_task,
    execute_assurance_snapshot as assurance_snapshot_task,
    execute_create_script as create_script_task,
    execute_change_analysis as change_analysis_task,
    execute_chat as send_message_task,
    execute_pan_to_prisma as pan_to_prisma_task,
)


# ----------------------------------------------------------------------------
# Define ViewSets for API endpoints
# ----------------------------------------------------------------------------
class PanoramaViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Panorama.objects.all()
    serializer_class = PanoramaSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                platform_name = request.data.get("platform")
                if platform_name:
                    platform = PanoramaPlatform.objects.get(name=platform_name)
                    serializer.validated_data["platform"] = platform
                serializer.save(author=self.request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PanoramaPlatformViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = PanoramaPlatform.objects.all()
    serializer_class = PanoramaPlatformSerializer


class PrismaViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Prisma.objects.all()
    serializer_class = PrismaSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(author=self.request.user)  # Change this line
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FirewallViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Firewall.objects.all()
    serializer_class = FirewallSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                platform_name = request.data.get("platform")
                if platform_name:
                    platform = FirewallPlatform.objects.get(name=platform_name)
                    serializer.validated_data["platform"] = platform
                serializer.save(author=self.request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FirewallPlatformViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = FirewallPlatform.objects.all()
    serializer_class = FirewallPlatformSerializer


class JobsViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Jobs.objects.all()
    serializer_class = JobsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(author=self.request.user)  # Change this line
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, format=None):
        instance = self.get_object()
        if instance.json_data is None:
            return JsonResponse({}, status=200)

        response_data = {
            "task_id": instance.task_id,
            "job_type": instance.job_type,
            "created_at": instance.created_at.isoformat(),
            "json_data": instance.json_data if instance.json_data is not None else {},
        }

        return JsonResponse(response_data, status=200)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return get_user_model().objects.all()
        else:
            return get_user_model().objects.filter(id=user.id)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class UserProfileView(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def retrieve(self, request, pk=None, format=None):
        conversation = Conversation.objects.get(pk=pk)
        message = conversation.messages.order_by("-index").first()
        serializer = self.get_serializer(message)
        return Response(serializer.data)


class ScriptViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrReadOnly,)
    serializer_class = ScriptSerializer

    def get_queryset(self):
        queryset = Script.objects.all()

        name = self.request.query_params.get("name", None)
        if name is not None:
            queryset = queryset.filter(name=name)

        return queryset


class FirewallExistsView(APIView):
    """
    A view that returns the existence of a firewall item by name as a boolean.
    """

    def get(self, request, format=None):
        raw_firewall_hostname = request.GET.get("hostname", None)
        if raw_firewall_hostname is not None:
            formatted_firewall_hostname = (
                raw_firewall_hostname.lower().replace(" ", "_").replace("-", "_")
            )
            exists = (
                Firewall.objects.annotate(
                    formatted_hostname=Replace(
                        Replace(Lower("hostname"), V(" "), V("_")), V("-"), V("_")
                    )
                )
                .filter(formatted_hostname=formatted_firewall_hostname)
                .exists()
            )
            return Response(
                {"exists": exists, "formatted_value": formatted_firewall_hostname}
            )
        else:
            return Response(
                {"error": "No firewall hostname provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class PanoramaExistsView(APIView):
    """
    A view that returns the existence of a panorama item by name as a boolean.
    """

    def get(self, request, format=None):
        raw_panorama_hostname = request.GET.get("hostname", None)
        if raw_panorama_hostname is not None:
            formatted_panorama_hostname = (
                raw_panorama_hostname.lower().replace(" ", "_").replace("-", "_")
            )
            exists = (
                Panorama.objects.annotate(
                    formatted_hostname=Replace(
                        Replace(Lower("hostname"), V(" "), V("_")), V("-"), V("_")
                    )
                )
                .filter(formatted_hostname=formatted_panorama_hostname)
                .exists()
            )
            return Response(
                {"exists": exists, "formatted_value": formatted_panorama_hostname}
            )
        else:
            return Response(
                {"error": "No panorama hostname provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )


# ----------------------------------------------------------------------------
# Define API endpoints for executing tasks
# ----------------------------------------------------------------------------


# Get System Info from Panorama
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def execute_get_system_info(request):
    pan_url = request.data.get("pan_url")
    api_key = request.data.get("api_key")
    author_id = request.user.id

    task = get_system_info_task.delay(pan_url, api_key, author_id)

    task_id = task.id

    return Response(
        {"message": "Task has been executed", "task_id": task_id},
        status=status.HTTP_200_OK,
    )


# Retrieve Certificate Chain
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def execute_upload_cert_chain(request):
    api_key = request.data.get("api_key")
    author_id = request.user.id
    pan_url = request.data.get("pan_url")
    url = request.data.get("url")

    task = upload_cert_chain_task.delay(api_key, author_id, pan_url, url)

    task_id = task.id

    return Response(
        {"message": "Task has been executed", "task_id": task_id},
        status=status.HTTP_200_OK,
    )


# Sync Panorama to Prsima
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def execute_pan_to_prisma(request):
    pan_url = request.data.get("pan_url")
    api_key = request.data.get("api_key")
    client_id = request.data.get("client_id")
    client_secret = request.data.get("client_secret")
    tsg_id = request.data.get("tsg_id")
    token_url = request.data.get("token_url")
    config_objects = request.data.get("config_objects")
    author_id = request.user.id

    task = pan_to_prisma_task.delay(
        pan_url,
        api_key,
        client_id,
        client_secret,
        tsg_id,
        token_url,
        config_objects,
        author_id,
    )

    task_id = task.id

    return Response(
        {"message": "Task has been executed", "task_id": task_id},
        status=status.HTTP_200_OK,
    )


# Assurance ARP Execution
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def execute_assurance_arp(request):
    # Use hostname from request to get api_key and IPv4 address
    hostname = request.data.get("hostname")
    try:
        firewall_instance = Firewall.objects.get(hostname=hostname)
        api_key = firewall_instance.api_key
        hostname = firewall_instance.ipv4_address
    except Firewall.DoesNotExist:
        return Response(
            {"message": "Firewall with the given hostname does not exist."},
            status=status.HTTP_404_NOT_FOUND,
        )
    operation_type = "readiness_check"
    action = "arp_entry_exist"
    config = request.data.get("config")
    author_id = request.user.id

    # Execute task
    task = assurance_arp_entry_task.delay(
        hostname,
        api_key,
        operation_type,
        action,
        config,
        author_id,
    )

    task_id = task.id

    return Response(
        {"message": "Task has been executed", "task_id": task_id},
        status=status.HTTP_200_OK,
    )


# Assurance Readiness
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def execute_assurance_readiness(request):
    # Use hostname from request to get api_key and IPv4 address
    hostname = request.data.get("hostname")
    try:
        firewall_instance = Firewall.objects.get(hostname=hostname)
        api_key = firewall_instance.api_key
        hostname = firewall_instance.ipv4_address
    except Firewall.DoesNotExist:
        return Response(
            {"message": "Firewall with the given hostname does not exist."},
            status=status.HTTP_404_NOT_FOUND,
        )
    operation_type = "readiness_check"
    config = request.data.get("config")
    author_id = request.user.id

    # Fetch the 'types' from the request payload
    types = request.data.get("types", {})

    # Check if the "all" key is true
    if types.get("all", False):
        # If "all" is true, include all keys except "all" itself
        action = ",".join([key for key in types.keys() if key != "all"])
    else:
        # If "all" is not true, filter out keys with true values
        action = ",".join([key for key, value in types.items() if value])

    # Execute task
    task = assurance_readiness_task.delay(
        hostname,
        api_key,
        operation_type,
        action,
        config,
        author_id,
    )

    task_id = task.id

    return Response(
        {"message": "Task has been executed", "task_id": task_id},
        status=status.HTTP_200_OK,
    )


# Assurance Snapshot
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def execute_assurance_snapshot(request):
    # Use hostname from request to get api_key and IPv4 address
    hostname = request.data.get("hostname")
    try:
        firewall_instance = Firewall.objects.get(hostname=hostname)
        api_key = firewall_instance.api_key
        hostname = firewall_instance.ipv4_address
    except Firewall.DoesNotExist:
        return Response(
            {"message": "Firewall with the given hostname does not exist."},
            status=status.HTTP_404_NOT_FOUND,
        )
    operation_type = "state_snapshot"
    # `config` is not within the body of this operation but is included for consistency
    config = request.data.get("config")
    author_id = request.user.id

    # Fetch the 'types' from the request payload
    types = request.data.get("types", {})

    # Check if the "all" key is true
    if types.get("all", False):
        # If "all" is true, include all keys except "all" itself
        action = ",".join([key for key in types.keys() if key != "all"])
    else:
        # If "all" is not true, filter out keys with true values
        action = ",".join([key for key, value in types.items() if value])

    # Execute task
    task = assurance_snapshot_task.delay(
        hostname,
        api_key,
        operation_type,
        action,
        config,
        author_id,
    )

    task_id = task.id

    return Response(
        {"message": "Task has been executed", "task_id": task_id},
        status=status.HTTP_200_OK,
    )


# Report of Administrators
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def execute_admin_report(request):
    pan_url = request.data.get("pan_url")
    api_key = request.data.get("api_key")
    to_emails = request.data.get("to_emails")
    author_id = request.user.id

    task = admin_report_task.delay(
        pan_url,
        api_key,
        to_emails,
        author_id,
    )

    task_id = task.id

    return Response(
        {"message": "Task has been executed", "task_id": task_id},
        status=status.HTTP_200_OK,
    )


# Create Script
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def execute_create_script(request):
    message = request.data.get("message")
    language = request.data.get("language")
    target = request.data.get("target")
    author_id = request.user.id

    task = create_script_task.delay(
        language,
        message,
        target,
        author_id,
    )

    task_id = task.id

    return Response(
        {"message": "Task has been executed", "task_id": task_id},
        status=status.HTTP_200_OK,
    )


# Change Analysis
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def execute_change_analysis(request):
    after_snapshot_id = request.data.get("afterSnapshot")
    before_snapshot_id = request.data.get("beforeSnapshot")
    message = request.data.get("message")
    expertise_level = request.data.get("expertiseLevel")
    author_id = request.user.id

    task = change_analysis_task.delay(
        after_snapshot_id,
        before_snapshot_id,
        message,
        expertise_level,
        author_id,
    )

    task_id = task.id

    return Response(
        {"message": "Task has been executed", "task_id": task_id},
        status=status.HTTP_200_OK,
    )


# Send Message to AI
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def execute_chat(request):
    author_id = request.data.get("author_id")
    conversation_id = request.data.get("conversation_id")
    llm = request.data.get("llm")
    message = request.data.get("message")
    persona = request.data.get("persona")

    # Use get_or_create to ensure Conversation instance exists
    convo, created = Conversation.objects.get_or_create(
        conversation_id=conversation_id,
        defaults={"author_id": author_id},  # provide author_id here
    )

    # If a new Conversation instance was created, you might want to set additional fields here
    if created:
        convo.save()

    task = send_message_task.delay(
        author_id,
        conversation_id,
        llm,
        message,
        persona,
    )

    task_id = task.id

    return Response(
        {
            "message": "Task has been executed",
            "conversation_id": conversation_id,
            "task_id": task_id,
        },
        status=status.HTTP_200_OK,
    )
