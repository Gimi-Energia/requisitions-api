def generateEmailTemplates(instance):
    
    software_names = "Nenhum"
    is_replacement = "Não"
    has_pc = "Não"
    needs_phone = "Não"
    needs_tablet = "Não"
    has_workstation = "Não"
    replaced_email = ""
    complete_name = instance.complete_name
    
    if len(instance.software_names) > 0:
        software_names = instance.software_names

    if instance.is_replacement:
        is_replacement = "Sim"
        replaced_email = f"<li>E-mail substituído: {instance.replaced_email}</li>"
    
    if instance.has_pc:
        has_pc = "Sim"

    if instance.needs_phone:
        needs_phone = "Sim"
    
    if instance.needs_tablet:
        needs_tablet = "Sim"
    
    if instance.has_workstation:
        has_workstation = "Sim"
    

    TEMPLATES = {
        "email_body_intro": {
            "Opened": f"<p>Foi criada uma nova requisição de funcionário por {instance.requester.name}</p>",  # noqa: E501
            "Pending": "<p>Há uma requisição de novo funcionário pendente.</p>",
            "Approved": f"<p>A requisição de funcionário foi aprovada por {instance.approver.name}. O processo pode seguir. Favor, cada setor, tomar as seguintes providências:</p>",  # noqa: E501
            "Denied": f"<p>A requisição foi negada por {instance.approver}</p>",
            "Canceled": "<p>A requisição de novo funcionário foi cancelada.</p>",
        },
        
        "summary_body": f"""
            <h2>Dados da solicitação:</h2>
            Empresa: {instance.company}<br>
            Departamento: {instance.cost_center.id} - {instance.cost_center.name}<br>
            Cargo: {instance.position.position}<br>
            Data solicitada: {instance.request_date.strftime("%d/%m/%Y")}<br>
            Número de controle: {instance.control_number}<br>
            Motivo: {instance.motive}<br>
            Requisitante: {instance.requester}<br>
            Aprovador: {instance.approver}<br>
            Observações: {instance.obs}<br>
        """,

        "RH": {
            "Pending": """
                <h3>RH</h3>
                <ul>
                    <li>Abrir a vaga para o candidato selecionado.</li>
                    <li>Entrar em contato com o getor do setor</li>
                </ul>
                <br>
            """,
            "Opened": "<br>",
            "Approved": "<br>",
            "Denied": "<br>",
            "Canceled": "<br>",
        },

        "TI": {
            "Pending": f"""
                <h3>TI</h3>
                <ul>
                    <li>Verificar equipamentos</li>
                    <li>Verificar estoque ou reserva</li>
                    <li>Necessidade de compra</li>
                    <li>Lead time médio</li>
                    <li>Softwares necessários: {software_names}</li>
                    <li>Tem PC: {has_pc}</li>
                    <li>Precisa Telefone: {needs_phone}</li>
                    <li>Precisa Tablet: {needs_tablet}</li>
                    <li>Tem estação de trabalho: {has_workstation}</li>
                </ul>
                <br>
            """,

            "Approved": f"""
                <h3>TI</h3>
                <ul>
                    <li>Criar e-mail</li>
                    <li>Criar login nos softwares</li>
                    <li>Criar login no ERP</li>
                </ul>
                <h4>Dados:</h4>
                <ul>
                    <li>Nome Completo: {complete_name}</li>
                    <li>Reposição: {is_replacement}</li>
                    {replaced_email}
                </ul>
                <br>
            """,

            "Opened": "<br>",
            "Denied": "<br>",
            "Canceled": "<br>",
        }
    }
    
    return TEMPLATES
