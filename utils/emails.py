from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.urls import reverse


class Mailing:

    def welcome_new_user_email(self, user, username, password):
        try:
            email_content = f"""
            <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        background-color: #f0f8ff;
                        padding: 10px;
                        margin: 0;
                    }}
                    .wrapper {{
                        background-color: #f0f8ff;
                        padding: 10px;
                        margin: 0 auto;
                        max-width: 600px;
                    }}
                    .card {{
                        background-color: white;
                        padding: 20px;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                        border-radius: 10px;
                        margin-bottom: 20px;
                    }}
                    .btn {{
                        display: inline-block;
                        background-color: #007bff;
                        color: white;
                        padding: 10px 20px;
                        text-decoration: none;
                        border-radius: 5px;
                    }}
                    .footer {{
                        background-color: #333;
                        color: white;
                        padding: 20px;
                        text-align: center;
                        border-radius: 0 0 10px 10px;
                    }}
                </style>
            </head>
            <body>
                <div class="wrapper">
                    <div class="card">
                        <center>
                        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ40-lwTDIxuPYC2vDNDdJZofa_BOuJcFPxpw&s" alt="School Pay Logo">
                        </center>
                        <br>
                        Hi {user.first_name} {user.last_name},
                        <p>Welcome to School Pay! We are delighted to have you on board.</p>
                        <p>School Pay is your one-stop solution for managing school fee payments efficiently and securely.</p>
                        <p>Here are your login details:</p>
                        <ul>
                            <li><strong>Username:</strong> {username}</li>
                            <li><strong>Password:</strong> {password}</li>
                        </ul>
                        <p>Please keep this information safe and secure.</p>
                        <p>If you have any questions or need assistance, feel free to reach out to us. We're here to help!</p>
                        <p>Best Regards,<br>School Pay Team</p>
                    </div>

                    <div class="footer">
                        <p>Contact Us: 254788994249 | Help: help@encodeteck.com</p>
                        <p>Powered By Encode Tech</p>
                    </div>
                </div>
            </body>
            </html>
            """

            sent = send_mail(
                'UWEZOPAY',
                '',
                'info@schoolpay.com',
                [user.email],
                fail_silently=False,
                html_message=email_content,
            )
            return sent

        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return 0

    def send_payment_confirmation(self, parent, transaction, receipt):
        try:
            email_content = f"""
            <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        background-color: #f0f8ff;
                        padding: 10px;
                        margin: 0;
                    }}
                    .wrapper {{
                        background-color: #f0f8ff;
                        padding: 10px;
                        margin: 0 auto;
                        max-width: 600px;
                    }}
                    .card {{
                        background-color: white;
                        padding: 20px;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                        border-radius: 10px;
                        margin-bottom: 20px;
                    }}
                    .btn {{
                        display: inline-block;
                        background-color: #007bff;
                        color: white;
                        padding: 10px 20px;
                        text-decoration: none;
                        border-radius: 5px;
                    }}
                    .footer {{
                        background-color: #333;
                        color: white;
                        padding: 20px;
                        text-align: center;
                        border-radius: 0 0 10px 10px;
                    }}
                </style>
            </head>
            <body>
                <div class="wrapper">
                    <div class="card">
                        <center>
                        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ40-lwTDIxuPYC2vDNDdJZofa_BOuJcFPxpw&s" alt="School Pay Logo">
                        </center>
                        <br>
                        Hi {parent.first_name} {parent.last_name},
                        <p>We are delighted to welcome you on board!</p>
                        <p>We are pleased to inform you that your payment of <strong>{transaction.amount}</strong> has been successfully processed.</p>
                        <a class="btn" href="{receipt.file_url}">Click here to download your receipt</a>
                        <p>Please keep this information safe and secure.</p>
                        <p>If you have any questions or need assistance, please feel free to reach out to us. We're here to help!</p>
                        <p>Best Regards,<br>School Pay Team</p>
                    </div>

                    <div class="footer">
                        <p>Contact Us: +254 788 994 249 | Help: help@encodeteck.com</p>
                        <p>Powered By Encode Tech</p>
                    </div>
                </div>
            </body>
            </html>
            """

            sent = send_mail(
                f'PAYMENT UPDATE - {receipt.receipt_number}',
                '',
                'info@schoolpay.com',
                [parent.email],
                fail_silently=False,
                html_message=email_content,
            )
            return sent

        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return 0

    def new_user_email(self, first_name, email, username, password):
        try:
            email_content = f"""
                <html>
                <head>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            background-color: #f0f8ff;
                            padding: 10px;
                            margin: 0;
                        }}
                        .wrapper {{
                            background-color: #f0f8ff;
                            padding: 10px;
                            margin: 0 auto;
                            max-width: 600px;
                        }}
                        .card {{
                            background-color: white;
                            padding: 20px;
                            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                            border-radius: 10px;
                            margin-bottom: 20px;
                        }}
                        .btn {{
                            display: inline-block;
                            background-color: #007bff;
                            color: white;
                            padding: 10px 20px;
                            text-decoration: none;
                            border-radius: 5px;
                        }}
                        .footer {{
                            background-color: #333;
                            color: white;
                            padding: 20px;
                            text-align: center;
                            border-radius: 0 0 10px 10px;
                        }}
                    </style>
                </head>
                <body>
                    <div class="wrapper">
                        <div class="card">
                            <center>
                            <img src="https://pbs.twimg.com/profile_banners/1178224657209712640/1687967155/600x200">
                            </center>
                            <br>
                            Hi {first_name}
                            <p>Welcome to Kejani! We are thrilled to have you join our community of homeowners, renters, and real estate enthusiasts.
                            At Kejani, we strive to provide you with the best tools and resources to make your real estate journey seamless and enjoyable. Whether you're searching for your dream home, looking to rent a cozy apartment, or exploring investment opportunities, we're here to support you every step of the way.</p>
                                                    <p>Here's what you can expect from your Kejani experience:</P>
                                                     <ol>
                                    <li><strong>Personalized Recommendations:</strong> Our intelligent recommendation system will help you discover properties that match your preferences and requirements.</li>
                                    <li><strong>Detailed Property Listings:</strong> Explore detailed property listings with high-quality photos, virtual tours, and comprehensive descriptions to make informed decisions.</li>
                                    <li><strong>Seamless Communication:</strong> Connect with real estate agents, landlords, and fellow users effortlessly through our messaging platform.</li>
                                    <li><strong>Expert Advice:</strong> Access expert advice, market insights, and helpful tips from industry professionals to guide you through your real estate journey.</li>
                                    <li><strong>Secure Transactions:</strong> Rest assured that your transactions are secure and protected with our robust security measures.</li>
                                </ol>
                                <p>We're committed to providing you with a superior real estate experience and helping you find the perfect place to call home.</p>
                                <p>If you have any questions or concerns, please don't hesitate to reach out to us. We're here to help!</p>

                            <h3>Login Details</h3>
                            <p>Username: {username}</p>
                            <p>Password: {password}</p>
                            <a href="http://176.97.114.193:8000/login" class="btn">Click here to log In</a>
                            <p>Best Regards <br>Kejani Team</p>
                        </div>

                        <div class="footer">
                            <p>Contact Us: 254711223344 | Help: help@encodeteck.com</p>
                            <p>Powered By Encode Tech</p>
                        </div>
                    </div>
                </body>
                </html>
                """

            sent = send_mail(
                f'Welcome to Kejani',
                '',
                'info@kejani.com',
                [email],
                fail_silently=False,
                html_message=email_content,
            )
            return sent

        except Exception as e:
            # response.setMessage(f"Error sending email: {str(e)}")
            sent = 0
            print(f"Error sending email: {str(e)}")
        return sent

    def reallocate_unit_email(self, tenant, unit):
        try:
            email_content = f"""
                <html>
                <head>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            background-color: #f0f8ff;
                            padding: 10px;
                            margin: 0;
                        }}
                        .wrapper {{
                            background-color: #f0f8ff;
                            padding: 10px;
                            margin: 0 auto;
                            max-width: 600px;
                        }}
                        .card {{
                            background-color: white;
                            padding: 20px;
                            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                            border-radius: 10px;
                            margin-bottom: 20px;
                        }}
                        .btn {{
                            display: inline-block;
                            background-color: green;
                            color: white;
                            padding: 10px 20px;
                            text-decoration: none;
                            border-radius: 5px;
                        }}
                        .footer {{
                            background-color: #333;
                            color: white;
                            padding: 20px;
                            text-align: center;
                            border-radius: 0 0 10px 10px;
                        }}
                    </style>
                </head>
                <body>
                    <div class="wrapper">
                        <div class="card">
                            <center>
                                <img src="https://pbs.twimg.com/profile_banners/1178224657209712640/1687967155/600x200" alt="Kejani">
                            </center>
                            <br>
                            <p>Dear {tenant.first_name},</p>
                            <p>Welcome to your new home at <strong>{unit.property.name} - House Number: {unit.name}</strong>! We are thrilled to have you as part of our community and hope you will find your new space comfortable and enjoyable.</p>
                            <p>Your new rent amount is <strong>{unit.rent}.00</strong>. If you have any questions or need assistance with settling in, please don't hesitate to reach out to us. We're here to help make your transition as smooth as possible.</p>
                            <p>Here are a few tips to get you started:</p>
                            <ul>
                                <li>Check out the amenities available in your new building.</li>
                                <li>Familiarize yourself with the local area and nearby services.</li>
                                <li>Join our community events and meet your new neighbors.</li>
                            </ul>
                            <p>For more information about your new home, kindly review it on our app or on your web account.</p>
                            <p>We look forward to supporting you and ensuring that you have a great experience living with us.</p>
                            <p>Best Regards,<br>Kejani Team</p>
                        </div>
                        <div class="footer">
                            <p>Contact Us: 254788994249 | Help: help@encodeteck.com</p>
                            <p>Powered By Encode Tech</p>
                        </div>
                    </div>
                </body>
                </html>
                """

            sent = send_mail(
                f'HOUSE TRANSFER {tenant.unit.property.name} - {tenant.unit.name}',
                '',
                'info@kejani.com',
                [tenant.email],
                fail_silently=False,
                html_message=email_content,
            )
            return sent
        except Exception as e:
            sent = 0
            print(f"Error sending email: {str(e)}")

    def account_deactivation(self, tenant):
        try:
            email_content = f"""
                <html>
                <head>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            background-color: #f0f8ff;
                            padding: 10px;
                            margin: 0;
                        }}
                        .wrapper {{
                            background-color: #f0f8ff;
                            padding: 10px;
                            margin: 0 auto;
                            max-width: 600px;
                        }}
                        .card {{
                            background-color: white;
                            padding: 20px;
                            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                            border-radius: 10px;
                            margin-bottom: 20px;
                        }}
                        .footer {{
                            background-color: #333;
                            color: white;
                            padding: 20px;
                            text-align: center;
                            border-radius: 0 0 10px 10px;
                        }}
                    </style>
                </head>
                <body>
                    <div class="wrapper">
                        <div class="card">
                            <center>
                                <img src="https://pbs.twimg.com/profile_banners/1178224657209712640/1687967155/600x200" alt="Kejani">
                            </center>
                            <br>
                            <p>Dear {tenant.first_name},</p>
                            <p>We hope this message finds you well.</p>
                            <p>We are writing to inform you that your account with Kejani has been deactivated as you have vacated from our property .</p>
                            <p>We appreciate the time you spent with us and hope you had a pleasant experience. If you have any pending matters or need assistance with your transition, please do not hesitate to reach out to us. Our team is here to support you during this period.</p>
                            <p>Please note that you can still access your account for the next 30 days to download any necessary documents or settle any outstanding balances. After this period, your account will be permanently closed.</p>
                            <p>If you have any questions or require further information, feel free to contact us. We are here to help.</p>
                            <p>Thank you for choosing Kejani, and we wish you all the best in your future endeavors.</p>
                            <p>Best Regards,<br>Kejani Team</p>
                        </div>
                        <div class="footer">
                            <p>Contact Us: 254788994249 | Help: help@encodeteck.com</p>
                            <p>Powered By Encode Tech</p>
                        </div>
                    </div>
                </body>
                </html>
                """

            sent = send_mail(
                'ACCOUNT DEACTIVATION NOTICE',
                '',
                'info@kejani.com',
                [tenant.email],
                fail_silently=False,
                html_message=email_content,
            )
            return sent
        except Exception as e:
            sent = 0
            print(f"Error sending email: {str(e)}")

    def welcome_back_activation_email(self, user):
        try:
            email_content = f"""
                <html>
                <head>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            background-color: #f0f8ff;
                            padding: 10px;
                            margin: 0;
                        }}
                        .wrapper {{
                            background-color: #f0f8ff;
                            padding: 10px;
                            margin: 0 auto;
                            max-width: 600px;
                        }}
                        .card {{
                            background-color: white;
                            padding: 20px;
                            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                            border-radius: 10px;
                            margin-bottom: 20px;
                        }}
                        .footer {{
                            background-color: #333;
                            color: white;
                            padding: 20px;
                            text-align: center;
                            border-radius: 0 0 10px 10px;
                        }}
                    </style>
                </head>
                <body>
                    <div class="wrapper">
                        <div class="card">
                            <center>
                                <img src="https://pbs.twimg.com/profile_banners/1178224657209712640/1687967155/600x200" alt="Kejani">
                            </center>
                            <br>
                            <p>Dear {user.first_name},</p>
                            <p>Welcome back to Kejani!</p>
                            <p>We are thrilled to inform you that your account has been successfully activated. You can now access all the features and benefits of being a member of our community.</p>
                            <p>If you have any questions, need assistance, or simply want to say hello, feel free to reach out to us. Our team is here to help make your experience with Kejani enjoyable and hassle-free.</p>
                            <p>Thank you for choosing Kejani. We look forward to serving you again!</p>
                            <p>Best Regards,<br>Kejani Team</p>
                        </div>
                        <div class="footer">
                            <p>Contact Us: 254788994249 | Help: help@encodeteck.com</p>
                            <p>Powered By Encode Tech</p>
                        </div>
                    </div>
                </body>
                </html>
                """

            sent = send_mail(
                'Welcome Back to Kejani!',
                '',
                'info@kejani.com',
                [user.email],
                fail_silently=False,
                html_message=email_content,
            )
            return sent
        except Exception as e:
            sent = 0
            print(f"Error sending email: {str(e)}")

    def send_invoice_reminder(self, tenant, invoice, amount):
        try:
            email_content = f"""
                <html>
                <head>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            background-color: #f0f8ff;
                            padding: 10px;
                            margin: 0;
                        }}
                        .wrapper {{
                            background-color: #f0f8ff;
                            padding: 10px;
                            margin: 0 auto;
                            max-width: 600px;
                        }}
                        .card {{
                            background-color: white;
                            padding: 20px;
                            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                            border-radius: 10px;
                            margin-bottom: 20px;
                        }}
                        .footer {{
                            background-color: #333;
                            color: white;
                            padding: 20px;
                            text-align: center;
                            border-radius: 0 0 10px 10px;
                        }}
                        .button {{
                            display: inline-block;
                            background-color: #4CAF50;
                            color: white;
                            padding: 10px 20px;
                            text-align: center;
                            text-decoration: none;
                            border-radius: 5px;
                            margin-top: 10px;
                        }}
                    </style>
                </head>
                <body>
                    <div class="wrapper">
                        <div class="card">
                            <center>
                                <img src="https://pbs.twimg.com/profile_banners/1178224657209712640/1687967155/600x200" alt="Kejani">
                            </center>
                            <br>
                            <p>Dear {tenant.first_name},</p>
                            <p>This is a friendly reminder that your invoice <strong>{invoice.invoice_number}</strong
                            > is due for payment.</p> <p>The total amount due is <strong>Ksh {amount}</strong>.</p>
                            <p>Please click the button below to proceed with payment:</p>
                            <center>
                                <a href="https://yourpaymentlink.com" class="button">Click here to pay</a>
                            </center>
                            <br>
                            <p>If you have already made the payment, please disregard this message.</p>
                            <p>Thank you for your prompt attention to this matter.</p>
                            <p>Best Regards,<br>Kejani Team</p>
                        </div>
                        <div class="footer">
                            <p>Contact Us: 254788994249 | Help: help@encodeteck.com</p>
                            <p>Powered By Encode Tech</p>
                        </div>
                    </div>
                </body>
                </html>
                """

            sent = send_mail(
                f'INVOICE REMINDER - {invoice.invoice_number}',
                '',
                'info@kejani.com',
                [tenant.email],
                fail_silently=False,
                html_message=email_content,
            )
            return sent
        except Exception as e:
            sent = 0
            print(f"Error sending email: {str(e)}")
