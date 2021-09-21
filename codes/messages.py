from flask import render_template, request, flash, session, url_for, redirect, jsonify
from views import *
from flask.views import View
import smtplib
from email.message import EmailMessage

rooms = ''
receiver = ''


class Chatting(View):

    def dispatch_request(self):

        if 'loggedin' in session:
            me = session['id']

            name = Conn.toProfile(me)
            myname = name.fullname

            #
            # chat list = get URL
            #
            inbox = db.session.query(chatrooms).filter(
                chatrooms.c.my_id == me).order_by(desc(chatrooms.c.id)).all()

            urId = []
            for i in inbox:

                # get id from fulnname
                stmt = db.session.query(User).filter(
                    User.fullname == i.user_name).first()
                urId.append(stmt.id)

            #
            # whose sending msg
            #
            checkMsg = db.session.query(chatrooms).filter(
                chatrooms.c.my_id == me).order_by(desc(chatrooms.c.id)).all()

            myMsg = []
            for i in checkMsg:

                if i.flag == "1":
                    myMsg.append(1)
                else:
                    myMsg.append(0)

            return render_template('/inbox.html', me=me, myname=myname, inbox=inbox, myMsg=myMsg, urId=urId, msgpage=True)

        return render_template('/login.html')

    def inbox(sendto):

        global rooms, receiver
        a = str(session['id'])
        b = str(sendto)
        receiver = b

        startchat = Conn.toProfile(b)
 
        history = db.session.query(Chat).filter(or_(
            Chat.chatroom == (a + "and" + b), Chat.chatroom == (b + "and" + a))).order_by(asc(Chat.id)).all()

        desc = ''
        boxDetail = ''
        if history:
            rooms = history[0].chatroom
            boxDetail = db.session.query(chatrooms).filter(
                chatrooms.c.ur_id == sendto).first()

            # show desc
            if boxDetail:
                x = Conn.toProfile(boxDetail.ur_id)
                desc = x.desc
                # send email (if user has send a message first time )

        else:
            rooms = (a + "and" + b)

            if rooms == (a+'and'+a) or rooms == (b+'and'+b):
                return redirect(url_for('inboxes'))
            else:

                aa = Conn.toProfile(a)
                bb = Conn.toProfile(b)
                if aa.role == bb.role:
                    return redirect(url_for('inboxes'))

        isRoom = db.session.query(Chat).filter(Chat.chatroom == rooms).first()
        if not isRoom:
            createTable = Chat(chatroom=rooms, message='Xx_st4rt|r00m_xX')
            db.session.add(createTable)
            db.session.commit()

        return render_template('/chat.html', me=a, desc=desc, boxDetail=boxDetail, history=history, rooms=rooms, startchat=startchat, msgpage=True)

    def message():

        if request.method == "POST":
            try:

                me = session['id']
                sender_id = request.form.get('sender_id')
                message = request.form.get('message')
                timesent = datetime.now()

                sender = Conn.toProfile(sender_id)
                pic = sender.pic

                # CREATE >> chat
                startchat = Chat(chatroom=rooms, sender_id=sender_id,
                                 message=message, pic=pic, date_time=timesent)
                db.session.add(startchat)

                ##################DATA######################
                user_sender = Conn.toProfile(me)
                myname = user_sender.fullname
                mypic = user_sender.pic

                user_tosend = Conn.toProfile(receiver)
                urid = user_tosend.id
                urname = user_tosend.fullname
                urpic = user_tosend.pic
                urmail = user_tosend.email
                ############################################

                # SEND >> E-MAIL ONCE at first
                send = db.session.query(chatrooms).filter(
                    chatrooms.c.room_id == rooms).first()
                if not send:
                    Chatting.sendMail(myname, urmail)

                # CLEAR >> sender chatroom (for new message)
                try:
                    del_sender = (delete(chatrooms).where(
                        chatrooms.c.my_id == me, chatrooms.c.room_id == rooms))
                    db.session.execute(del_sender)
                    db.session.commit()
                except:
                    pass

                # RECREATE >> chatroom

                # CREATE >> sender INBOX
                create_inbox = chatrooms.insert().values(my_id=me, ur_id=urid, user_pic=urpic, user_name=urname,
                                                         room_id=rooms, room_message=message, date_time=timesent, flag=True)
                db.session.execute(create_inbox)

                # UPDATE new message for receiver
                # CLEAR >> receiver chatroom (for new message)
                try:
                    del_receiver = (delete(chatrooms).where(
                        chatrooms.c.my_id == urid, chatrooms.c.room_id == rooms))
                    db.session.execute(del_receiver)
                    db.session.commit()
                except:
                    pass
                    print('failed')

                # CREATE NEW >> receiver chatroom (for new message)
                new_receiver = chatrooms.insert().values(my_id=urid, ur_id=me, user_pic=mypic, user_name=myname,
                                                         room_id=rooms, room_message=message, date_time=timesent, flag=False)
                db.session.execute(new_receiver)

                db.session.commit()
                print('commit All PASS')
                flags = str(me)

                pusher_client.trigger(
                    rooms, 'new-message', {'sender_id': sender_id, 'message': message, 'datetime': timesent.strftime('%H:%M u.'), 'pic': pic, 'flags': flags})

                return jsonify({'result': 'success'})

            except:

                return jsonify({'result': 'failure'})

    def sendMail(a, b):

        sender_name = a
        rec_email = b

        web = "yourpartner.no.reply@gmail.com"

        msg = EmailMessage()
        msg['Subject'] = 'คุณได้รับข้อความจาก :' + sender_name
        msg['From'] = web
        msg['To'] = rec_email

        msg.set_content(

            '{} เพิ่งได้ส่งข้อความหาคุณ เช็คกล่องข้อความเพื่อเริ่มสนทนากับ {} เลย!\n'
            'http://127.0.0.1:5000/inbox'.format(a, a)
        )

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(web, "yourpartner1234")
        server.send_message(msg)
        server.quit()
 

        # yourpartner.no.reply@gmail.com
        # pass: yourpartner1234
