login_otp_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Fleet Management</title>
</head>
<body style="margin: 0;">
    <div
    style=" line-height: 1.6;
        margin: 0; padding: 0;
        background-color: #f4f4f4;
        padding-top: 20px;
        padding-bottom: 20px;
     "
     >
        <div class="container"
            style="
                max-width: 580px;
                margin: 20px auto;
                padding: 10px;
                border-radius: 5px;
                background-color: #ffffff;
                box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
                color: #454748;
                font-family: Arial, Helvetica, sans-serif;
            "
            >
            <div class="header"
            style="
                padding: 2px;
                text-align: center;
                background-color: #8C162D;
            "
            >
                <img
                src="https://archholdings.com/wp-content/uploads/2023/07/ArchHoldings-21.png"
                alt="Newgas-logo"
                style="
                     width: 92px;
                    height: 65px;
                    object-fit: contain;
                "
                />
            </div>
            <hr style="background-color: #b1afaf; height: 1px; border: 0;"/>
            <div class="content"
             style="
                padding-left: 5px;
                padding-right: 5px;
                font-size: 17px;
            "
            >
                <p>Hello {{email}}</p>
                <div style="text-align: center;">
                    <p>Your Newgas One-Time Password (OTP) is:</p>
                    <!-- Center the OTP code and make it larger -->
                    <p class="otp-code"
                    style="
                        text-align: center;
                        font-size: 33px;
                        margin: 0;
                        color: #8C162D;
                    "
                    >
                        <strong>{{otp}}</strong>
                    </p>
                    <p>
                        This OTP is valid for a single use and will expire shortly. Please use it for the intended purpose only.
                        If you did not request this OTP, please disregard this email and ensure your account's security.
                    </p>
                </div>
            </div>
            <div class="button"
            style="
                display: flex;
                justify-content: center;
            "
            >
                <!-- <a href="#"
                style="
                    background-color: #D32129;
                    color: white;
                    border: none;
                    outline: none;
                    padding: 10px;
                    border-radius: 5px;
                    font-weight: 600;
                    text-decoration: none;
                "
                >
                    Activate Account
                </a> -->
            </div>
            <hr class="bottom-hr" style="background-color: #b1afaf; height: 1px; border: 0; margin-top: 35px;"/>
            <div class="footer"
            style="
                font-size: 15px;
                text-align: center;
                background-color: #8C162D;
                padding: 5px;
            "
            >
                <!-- <p>This email was sent to {{ email }}. If you have any questions, please contact support@example.com.</p> -->
                <a class="footer-p2"
                href="info@yourcompany.com"
                style="
                    margin-bottom: 0;
                    margin-top: 5px;
                    color: white;
                    text-decoration: none;

                "
                >
                    info@archholdings.com | <a href="https://archholdings.com/" style="color: white; text-decoration: none;">www.archholdings.com</a>
            </a>
            </div>
        </div>
    </div>
</body>
</html>


"""
